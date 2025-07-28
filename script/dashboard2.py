import streamlit as st
import pandas as pd
from bson import ObjectId
from datetime import datetime
import json
import os
import tempfile

from db import get_all_documents, update_document
from report import generate_pdf_report
def highlight_emergenza(row):
    if row.get("usage_mode", "").lower() == "emergenza":
        return ['background-color: #ffcccc'] * len(row)
    else:
        return [''] * len(row)

st.title("Tabella Clinica")

# --- Categorie dei campi ---
field_categories = {
    "Anagrafica": ["first_name", "last_name", "birth_date", "birth_place", "age", "gender", "residence_city", "residence_address", "phone"],
    "Accesso": ["access_mode"],
    "Condizioni": ["skin_state", "consciousness_state", "pupils_state", "respiratory_state"],
    "Storia clinica": ["history", "medications_taken", "symptoms"],
    "Parametri vitali": ["heart_rate", "oxygenation", "blood_pressure", "temperature", "blood_glucose"],
    "Tipo di Report": ["usage_mode"],
    "Diagnostica e trattamento": ["diagnostic_tests", "assessment", "plan", "triage_code"]
}

if "all_docs" not in st.session_state:
    st.session_state["all_docs"] = get_all_documents()

def unwrap_list(x):
    if isinstance(x, list):
        return x[0] if x else ""
    return x if isinstance(x, str) else ""

# --- Sidebar con filtri ---
with st.sidebar:
    st.header("Filtri per categoria")
    selected_fields = {}

    for category, fields in field_categories.items():
        st.markdown(f"---\n**{category}**")

        # Checkbox "Seleziona tutto"
        all_key = f"{category}_all"
        if all_key not in st.session_state:
            st.session_state[all_key] = False
        select_all = st.checkbox("Seleziona tutto", key=all_key)

        # Se viene cliccato "Seleziona tutto", aggiorna i checkbox figli
        if select_all and not all([st.session_state.get(f"{category}_{f}", False) for f in fields]):
            for field in fields:
                st.session_state[f"{category}_{field}"] = True

        with st.expander("Filtri specifici", expanded=False):
            for field in fields:
                field_key = f"{category}_{field}"
                default_active_fields = ["first_name", "last_name", "triage_code", "usage_mode","access_mode","consciousness_state"]

                if field_key not in st.session_state:
                    st.session_state[field_key] = field in default_active_fields

                selected = st.checkbox(field.replace("_", " ").capitalize(), key=field_key)
                selected_fields[field] = selected


# --- Campi attivi selezionati ---
active_fields = [f for f, selected in selected_fields.items() if selected]
field_inputs = {}

st.markdown("### Campi di Ricerca")

# Layout input dinamico
for i in range(0, len(active_fields), 3):
    cols = st.columns(3)
    for j, field in enumerate(active_fields[i:i+3]):
        with cols[j]:
            label = field.replace("_", " ").capitalize()
            values = set()
            for doc in st.session_state["all_docs"]:
                val = unwrap_list(doc.get(field, ""))
                if val:
                    values.add(val)
            values = sorted(values)
            field_inputs[field] = st.text_input(label, key=f"input_{field}")

# Visione tabella
@st.fragment(run_every="5s")
def refresh_table():
    docs = get_all_documents()
    docs.sort(key=lambda d: d["_id"], reverse=True)
    print(docs)
    rows = []
    for doc in docs:
        row = {"_id": doc["_id"]}
        for field in selected_fields.keys():
            row[field] = unwrap_list(doc.get(field, ""))
        if "usage_mode" not in selected_fields:
            row["usage_mode"] = unwrap_list(doc.get("usage_mode", ""))
        rows.append(row)

    df = pd.DataFrame(rows)

    for field in active_fields:
        val = field_inputs.get(field, "").strip()
        if val:
            df = df[df[field].astype(str).str.contains(val, case=False, na=False)]

    styled_df = df.style.apply(highlight_emergenza, axis=1)
    st.dataframe(styled_df, use_container_width=True)

    if not df.empty:
        # Salvataggio selezione precedente
        previous_selection = st.session_state.get("previous_selected_id", None)

        selected_id = st.selectbox(
            "Seleziona una riga da modificare o generare il report",
            df["_id"].astype(str).tolist(),
            key="selected_row"
        )

        # Reset del PDF se la selezione cambia
        if previous_selection != selected_id:
            st.session_state["pdf_ready"] = False
            st.session_state["generated_pdf"] = None
            st.session_state.pop("edit_doc", None)
            st.session_state.pop("edit_doc_id", None)
        st.session_state["previous_selected_id"] = selected_id

        # Checkbox per visualizzare la trascrizione
        show_transcription = st.checkbox("Visualizza trascrizione del report selezionato")

        if show_transcription and selected_id:
            selected_doc = next((doc for doc in docs if str(doc["_id"]) == selected_id), None)
            if selected_doc:
                transcription_text = unwrap_list(selected_doc.get("transcription", "Nessuna trascrizione disponibile."))
                st.markdown("### Trascrizione")
                st.text_area("Contenuto della trascrizione", value=transcription_text, height=300, disabled=True)

        # Pulsante aggiorna dati
        if st.button("Aggiorna dati", key="aggiorna_dati"):
            selected_doc = next((doc for doc in docs if str(doc["_id"]) == selected_id), None)
            if selected_doc:
                st.session_state["edit_doc"] = selected_doc
                st.session_state["edit_doc_id"] = selected_id

        # Pulsante genera report
        if st.button("📄 Genera Report PDF", key="generate_report"):
            selected_doc = next((doc for doc in docs if str(doc["_id"]) == selected_id), None)
            if selected_doc:
                try:
                    extracted_dict = {k: [unwrap_list(v)] for k, v in selected_doc.items() if k != "_id"}
                    extracted_dict["exit_date"] = [datetime.now().strftime("%d/%m/%Y %H:%M")]

                    pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
                    generate_pdf_report(extracted_dict, pdf_path)

                    with open(pdf_path, "rb") as f:
                        st.session_state["generated_pdf"] = f.read()
                    st.session_state["pdf_ready"] = True
                    os.unlink(pdf_path)

                except Exception as e:
                    st.error(f"Errore nella generazione del PDF: {e}")
                    st.session_state["pdf_ready"] = False

        # Mostra pulsante di download se PDF pronto
        if st.session_state.get("pdf_ready", False):
            st.success("📄 PDF generato con successo!")
            st.download_button(
                label="⬇️ Scarica PDF",
                data=st.session_state["generated_pdf"],
                file_name="clinical_report.pdf",
                mime="application/pdf"
            )

    # Se si sta modificando un documento
    if "edit_doc" in st.session_state:
        st.markdown("### Modifica dati documento")
        edited_data = {}
        for category, fields in field_categories.items():
            with st.expander(category):
                for field in fields:
                    current_val = unwrap_list(st.session_state["edit_doc"].get(field, ""))
                    new_val = st.text_input(field.replace("_", " ").capitalize(), value=current_val, key=f"edit_{field}")
                    edited_data[field] = new_val

        if st.button("Completa aggiornamento", key="completa_aggiornamento"):
            update_data = {k: v for k, v in edited_data.items()}
            try:
                update_document(ObjectId(st.session_state["edit_doc_id"]), update_data)
                st.success("Documento aggiornato con successo.")
                del st.session_state["edit_doc"]
                del st.session_state["edit_doc_id"]
                st.session_state["all_docs"] = get_all_documents()
            except Exception as e:
                st.error(f"Errore nell'aggiornamento: {e}")

refresh_table()
