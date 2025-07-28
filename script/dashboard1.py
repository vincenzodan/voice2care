import streamlit as st
import random
import tempfile
import os
from datetime import datetime
from transcription import transcribe_audio
from extraction import parse_generated_json, extract_all, validate_fields, normalize_fields
from db import save_to_mongo
from report import generate_pdf_report, generate_pdf_checkup
from st_audiorec import st_audiorec
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment
# import gc
import torch

# gc.collect()
torch.cuda.empty_cache()


def safe_get(key):
    extracted_dict = st.session_state.get("extracted_dict", {})
    value = extracted_dict.get(key)
    if isinstance(value, list):
        return value[0] if value else ""
    return value if value is not None else ""


def text_input_with_error(label, key, col, errors):
    with col:
        value_extracted = safe_get(key)
        value = st.text_input(label, value=safe_get(key))
        if key in errors and value != value_extracted:  # Se c'è un valore valido ora
            errors.remove(key)  # Rimuovi l'errore se il campo è stato riempito
            st.session_state["errors"] = errors
        elif key in errors:
            st.markdown(f"<span style='color:red'>⚠️ Errore nel campo {label}</span>", unsafe_allow_html=True)
    return value


st.set_page_config(page_title="Clinical Audio Dashboard", layout="wide")
st.title("🩺 Clinical Audio Transcription & Extraction Dashboard")

with st.sidebar:
    st.markdown("### 🔧 Modalità di utilizzo")
    usage_mode = st.radio("Scegli la modalità:", ["Report", "Checkup", "Emergenza"])

    st.markdown("---")  # linea divisoria opzionale
    st.markdown("### 🎙️ Input Audio")
    choice = st.radio("Metodo di inserimento audio:", ["Upload audio file", "Record audio"])

audio_bytes = None


if choice == "Upload audio file":
    with st.sidebar:
        uploaded_file = st.file_uploader("📄 Upload an audio file (wav or mp3)", type=["wav", "mp3"],
                                         label_visibility="visible",
                                         help="Per caricare un nuovo file clicca sulla x per eliminare quello precedente!")
        st.caption("Per caricare un nuovo file elimina prima il precedente!")

    if not uploaded_file and "uploaded_file" in st.session_state:
        del st.session_state["uploaded_file"]
        del st.session_state["audio_bytes"]

    if uploaded_file and "uploaded_file" not in st.session_state:
        audio_bytes = uploaded_file.read()
        st.session_state["uploaded_file"] = uploaded_file
        st.session_state["audio_bytes"] = audio_bytes
        st.audio(audio_bytes)

        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tfile.write(audio_bytes)
        tfile.close()

        with st.spinner("📝 Transcribing audio..."):
            transcription = transcribe_audio(tfile.name)

        with st.spinner("🔎 Extracting clinical information..."):
            extracted_text = extract_all(transcription)
            extracted_dict = parse_generated_json(extracted_text)
            if extracted_dict != None:
                extracted_dict = normalize_fields(extracted_dict, usage_mode)
                errors = validate_fields(extracted_dict, transcription)
            if extracted_dict == None:
                extracted_text = extract_all(transcription)
                extracted_dict = parse_generated_json(extracted_text)
                if extracted_dict != None:
                    extracted_dict = normalize_fields(extracted_dict, usage_mode)
                    errors = validate_fields(extracted_dict, transcription)
            if extracted_dict == None:
                st.error("❌ Prova a rifare l'audio")
                st.stop()
        extracted_dict["usage_mode"] = usage_mode
        triage_date = os.path.getctime(tfile.name)
        triage_date = datetime.fromtimestamp(triage_date)
        triage_date = triage_date.strftime("%d/%m/%Y %H:%M")
        extracted_dict["triage_date"] = [triage_date]

        ID = random.randint(10 ** 10, 10 ** 11 - 1)
        extracted_dict["ID"] = [ID]

        st.session_state["transcription"] = transcription
        st.session_state["extracted_dict"] = extracted_dict
        st.session_state["transcription_ready"] = True
        st.session_state["errors"] = errors
        os.unlink(tfile.name)

    elif "uploaded_file" in st.session_state:
        st.audio(st.session_state["audio_bytes"])

elif choice == "Record audio":
    with st.sidebar:
        wav_audio_data = st.audio_input("🎧 Registra il tuo messaggio")

        st.caption("Elimina quello precedente per riniziare.")

    # Rimozione dell'audio registrato precedente se l'utente ne ha rimosso uno
    if not wav_audio_data and "recorded_audio" in st.session_state:
        del st.session_state["recorded_audio"]

    # Se è stato registrato un nuovo audio
    if wav_audio_data and "recorded_audio" not in st.session_state:
        st.session_state["recorded_audio"] = wav_audio_data
        st.audio(wav_audio_data)

        # Scrive i byte su file temporaneo WAV
        audio_bytes = wav_audio_data.getvalue()
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tfile.write(audio_bytes)
        tfile.close()

        with st.spinner("📝 Transcribing audio..."):
            transcription = transcribe_audio(tfile.name)

        with st.spinner("🔎 Extracting clinical information..."):
            extracted_text = extract_all(transcription)
            extracted_dict = parse_generated_json(extracted_text)

            if extracted_dict is not None:
                extracted_dict = normalize_fields(extracted_dict, usage_mode)
                errors = validate_fields(extracted_dict, transcription)
            else:
                # Tentativo di fallback (come per upload)
                extracted_text = extract_all(transcription)
                extracted_dict = parse_generated_json(extracted_text)
                if extracted_dict is not None:
                    extracted_dict = normalize_fields(extracted_dict, usage_mode)
                    errors = validate_fields(extracted_dict, transcription)

            if extracted_dict is None:
                st.error("❌ Prova a rifare la registrazione.")
                os.unlink(tfile.name)
                st.stop()

        # Aggiunta metadati
        extracted_dict["usage_mode"] = usage_mode
        triage_date = datetime.fromtimestamp(os.path.getctime(tfile.name)).strftime("%d/%m/%Y %H:%M")
        extracted_dict["triage_date"] = [triage_date]
        extracted_dict["ID"] = [random.randint(10**10, 10**11 - 1)]

        # Salvataggio nei dati di sessione
        st.session_state["transcription"] = transcription
        st.session_state["extracted_dict"] = extracted_dict
        st.session_state["transcription_ready"] = True
        st.session_state["errors"] = errors

        os.unlink(tfile.name)

    # Audio già registrato presente in sessione
    elif "recorded_audio" in st.session_state:
        st.audio(st.session_state["recorded_audio"])


if "transcription_ready" in st.session_state and st.session_state.transcription_ready:
    st.subheader("📃 Transcription")
    st.write(st.session_state.transcription)

    extracted_dict = st.session_state.extracted_dict
    errors = st.session_state.errors
    if usage_mode !="Checkup":

        st.subheader("🧠 Review and Complete Patient Information")

        st.markdown("### 📄 Relazione Clinica")
        col_id, col_date = st.columns([2, 1])
        ID = st.text_input("N. VERBALE", value=safe_get("ID"))

        st.markdown("### 👤 Dati Anagrafici Assistito")
        col1, col2, col3 = st.columns(3)
        last_name = text_input_with_error("Cognome", "last_name", col1, errors)
        birth_date = text_input_with_error("Data di nascita", "birth_date", col1, errors)
        first_name = text_input_with_error("Nome", "first_name", col2, errors)
        birth_place = text_input_with_error("Luogo di nascita", "birth_place", col2, errors)
        age = text_input_with_error("Età", "age", col3, errors)
        gender = text_input_with_error("Sesso", "gender", col3, errors)

        st.markdown("### 🏠 Contatti e Residenza")
        col4, col5, col6 = st.columns(3)
        residence_city = text_input_with_error("Città di residenza", "residence_city", col4, errors)
        residence_address = text_input_with_error("Indirizzo", "residence_address", col5, errors)
        phone = text_input_with_error("Telefono", "phone", col6, errors)

        st.markdown("### 🚑 Accesso")
        col8, col9 = st.columns(2)
        symptoms = text_input_with_error("Motivo dell'accesso (Sintomi)", "symptoms", col8, errors)
        access_mode = text_input_with_error("Modalità di accesso", "access_mode", col9, errors)

        # === DATE E URGENZE ===
        st.markdown("### 🕒 Date e Urgenze")
        col10, col12 = st.columns(2)
        with col10:
            triage_date = st.text_input("Data triage", value=safe_get("triage_date"))

        with col12:
            exit_date = st.text_input("Data uscita", value=safe_get("exit_date"))

        col13, col14 = st.columns(2)
        with col13:
            triage_code = st.text_input("Codice triage", value=safe_get("triage_code"))
        with col14:
            discharge_code = st.text_input("Codice dimissione", value=safe_get("discharge_code"))

        # === ANAMNESI ===
        st.markdown("### 📝 Anamnesi")
        history = st.text_input("Storia clinica", value=safe_get("history"))
        medications_taken = st.text_input("Medications", value=safe_get("medications_taken"))

        # === RILEVAZIONI CLINICHE ===

        st.markdown("### 🩺 Rilevazioni Cliniche")
        col15, col16 = st.columns(2)
        consciousness_state = text_input_with_error("Coscienza", "consciousness_state", col15, errors)
        respiratory_state = text_input_with_error("Respiro", "respiratory_state", col15, errors)
        skin_state = text_input_with_error("Cute", "skin_state", col15, errors)
        pupils_state = text_input_with_error("Pupille", "pupils_state", col15, errors)

        oxygenation = text_input_with_error("Saturazione", "oxygenation", col16, errors)
        heart_rate = text_input_with_error("Frequenza cardiaca (heart_rate)", "heart_rate", col16, errors)
        temperature = text_input_with_error("Temperatura corporea (°C)", "temperature", col16, errors)
        blood_pressure = text_input_with_error("Pressione Arteriosa (mmHg)", "blood_pressure", col16, errors)
        blood_glucose = text_input_with_error("Glicemia (Mg/dl)", "blood_glucose", col16, errors)

        st.markdown("### 🩹 Piano Clinico e Azioni")
        medical_actions = st.text_input("Medical actions", value=safe_get("medical_actions"))
        plan = st.text_input("Plan", value=safe_get("plan"))
        assessment = st.text_input("Assessment", value=safe_get("assessment"))

        # === NOTE FINALI ===
        st.markdown("### 📌 Note e Prescrizioni")
        annotations = st.text_area("Annotazioni", value=safe_get("annotations"), height=100)

    else:
        st.markdown("### 📄 Monitoraggio Giornaliero")
        data_checkup = st.text_input("Data Visita:", value=datetime.now().strftime("%d/%m/%Y %H:%M"))

        st.markdown("### 👤 Dati Anagrafici Assistito")
        col1, col2 = st.columns(2)
        last_name = text_input_with_error("Cognome", "last_name", col1, errors)
        first_name = text_input_with_error("Nome", "first_name", col2, errors)

        col3 = st.columns(1)[0]
        symptoms = text_input_with_error("Sintomi", "symptoms", col3, errors)
        medications_taken = st.text_input("Terapia in corso", value=safe_get("medications_taken"))

        st.markdown("### 🩺 Rilevazioni Cliniche")
        col15, col16 = st.columns(2)

        oxygenation = text_input_with_error("Saturazione", "oxygenation", col15, errors)
        heart_rate = text_input_with_error("Frequenza cardiaca (heart_rate)", "heart_rate", col15, errors)
        temperature = text_input_with_error("Temperatura corporea (°C)", "temperature", col15, errors)
        blood_pressure = text_input_with_error("Pressione Arteriosa (mmHg)", "blood_pressure", col16, errors)
        blood_glucose = text_input_with_error("Glicemia (Mg/dl)", "blood_glucose", col16, errors)

        st.markdown("### 🩹 Piano Clinico e Azioni")
        assessment = st.text_input("Assessment", value=safe_get("assessment"))
        medical_actions = st.text_input("Medical actions", value=safe_get("medical_actions"))
        plan = st.text_input("Plan", value=safe_get("plan"))
        
        # === NOTE FINALI ===
        st.markdown("### 📌 Note e Prescrizioni")
        annotations = st.text_area("Annotazioni", value=safe_get("annotations"), height=100)


    if st.button("💾 Save to MongoDB"):
        if usage_mode !="Checkup":
            extracted_dict.update({
                "first_name": [first_name], "last_name": [last_name], "birth_date": [birth_date],
                "birth_place": [birth_place], "age": [age], "gender": [gender], "triage_code": [triage_code],
                "discharge_code": [discharge_code], "residence_city": [residence_city],
                "residence_address": [residence_address], "phone": [phone], "triage_date": [triage_date],
                "access_mode": [access_mode], "consciousness_state": [consciousness_state], "usage_mode":[usage_mode],
                "respiratory_state": [respiratory_state], "skin_state": [skin_state], "pupils_state": [pupils_state],
                "oxygenation": [oxygenation], "heart_rate": [heart_rate], "blood_pressure": [blood_pressure],
                "blood_glucose": [blood_glucose], "temperature": [temperature],
                "medications_taken": [medications_taken], "symptoms": [symptoms], 
                "history": [history], "assessment": [assessment], "plan": [plan], "medical_actions":[medical_actions],
                "annotations": [annotations], "exit_date": [exit_date], "transcription": st.session_state.transcription
            })
        else:
            extracted_dict.update({
                "first_name": [first_name], "last_name": [last_name], 
                "usage_mode":[usage_mode],
                "oxygenation": [oxygenation], "heart_rate": [heart_rate], "blood_pressure": [blood_pressure],
                "blood_glucose": [blood_glucose], "temperature": [temperature],
                "medications_taken": [medications_taken], "symptoms": [symptoms], 
                "assessment": [assessment], "plan": [plan], "medical_actions":[medical_actions],
                "annotations": [annotations], "transcription": st.session_state.transcription
            })
        try:
            save_to_mongo(extracted_dict)
            st.success("✅ Data saved to MongoDB!")
        except Exception as e:
            st.error(f"❌ Error saving to MongoDB: {e}")

    if "generate_report_clicked" not in st.session_state:
        st.session_state.generate_report_clicked = False

    if st.button("📄 Generate PDF Report"):
        st.session_state.generate_report_clicked = True
        if st.session_state.generate_report_clicked:
            exit_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            if usage_mode !="Checkup":
                extracted_dict.update({
                    "first_name": [first_name], "last_name": [last_name], "birth_date": [birth_date],
                    "birth_place": [birth_place], "age": [age], "gender": [gender], "triage_code": [triage_code],
                    "discharge_code": [discharge_code], "residence_city": [residence_city],
                    "residence_address": [residence_address], "phone": [phone], "triage_date": [triage_date],
                    "access_mode": [access_mode], "consciousness_state": [consciousness_state], "usage_mode":[usage_mode],
                    "respiratory_state": [respiratory_state], "skin_state": [skin_state], "pupils_state": [pupils_state],
                    "oxygenation": [oxygenation], "heart_rate": [heart_rate], "blood_pressure": [blood_pressure],
                    "blood_glucose": [blood_glucose], "temperature": [temperature],
                    "medications_taken": [medications_taken], "symptoms": [symptoms], 
                    "history": [history], "assessment": [assessment], "plan": [plan], "medical_actions":[medical_actions],
                    "annotations": [annotations], "exit_date": [exit_date], "transcription": st.session_state.transcription
                })
            else:
                extracted_dict.update({
                    "first_name": [first_name], "last_name": [last_name], 
                    "usage_mode":[usage_mode],
                    "oxygenation": [oxygenation], "heart_rate": [heart_rate], "blood_pressure": [blood_pressure],
                    "blood_glucose": [blood_glucose], "temperature": [temperature],
                    "medications_taken": [medications_taken], "symptoms": [symptoms], 
                    "assessment": [assessment], "plan": [plan], "medical_actions":[medical_actions],
                    "annotations": [annotations], "transcription": st.session_state.transcription
                })
            try:
                pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
                if usage_mode == "Checkup":
                    generate_pdf_checkup(extracted_dict, pdf_path)
                else:
                    generate_pdf_report(extracted_dict, pdf_path)
                st.success("📄 PDF Report generated!")
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(label="⬇️ Download PDF Report", data=pdf_file, file_name="clinical_report.pdf",
                                       mime="application/pdf")
                os.unlink(pdf_path)
            except Exception as e:
                st.error(f"❌ Error generating PDF: {e}")