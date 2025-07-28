import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime
from dateutil.parser import parse
import re
import json
#from huggingface_hub import InferenceClient
from huggingface_hub import login
import config

login(token=config.HUGGINGFACE_TOKEN)

# Se in locale meglio un modello più leggero
#model_name = "google/gemma-3-1b-it"
model_name = "google/gemma-2-2b-it"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
    device_map="auto"
)


def normalize_fields(data: dict, usage_mode: str = "") -> dict:
    normalized = data.copy()
    null_values = {"unknown", "na", "n/a", "null", "none"}
    # Rimuove valori considerati nulli (case-insensitive) da tutti i campi
    for key, value in normalized.items():
        if isinstance(value, str) and value.strip().lower() in null_values and len(value.strip().split()) == 1:
            normalized[key] = ""

    # Frequenza cardiaca
    if data.get("heart_rate"):
        match = re.search(r"\b(\d{2,3})\b", str(data["heart_rate"]))
        normalized["heart_rate"] = int(match.group(1)) if match else ""
    else:
        normalized["heart_rate"] = ""

    # Saturazione di ossigeno (numero + % se presente, se manca % lo aggiunge)
    if data.get("oxygenation"):
        value = str(data["oxygenation"])
        match = re.search(r"\b(\d{1,3})\b", value)
        if match:
            oxy_value = match.group(1)
            normalized["oxygenation"] = f"{oxy_value}%"  # Aggiunge il simbolo %
        else:
            normalized["oxygenation"] = ""
    else:
        normalized["oxygenation"] = ""

    # Temperatura
    if data.get("temperature"):
        value = str(data["temperature"]).replace(",", ".")
        match = re.search(r"([-+]?\d+(\.\d+)?)", value)
        normalized["temperature"] = float(match.group(1)) if match else ""
    else:
        normalized["temperature"] = ""

    # Glicemia
    if data.get("blood_glucose"):
        match = re.search(r"\b(\d{2,3})\b", str(data["blood_glucose"]))
        normalized["blood_glucose"] = int(match.group(1)) if match else ""
    else:
        normalized["blood_glucose"] = ""

    # Pressione arteriosa: se due numeri senza /, lo aggiunge
    if data.get("blood_pressure"):
        value = str(data["blood_pressure"])
        if "/" in value:
            match = re.search(r"\b(\d{2,3})\s*/\s*(\d{2,3})\b", value)
            normalized["blood_pressure"] = f"{match.group(1)}/{match.group(2)}" if match else ""
        else:
            match = re.findall(r"\b(\d{2,3})\b", value)
            if len(match) == 2:
                normalized["blood_pressure"] = f"{match[0]}/{match[1]}"
            else:
                normalized["blood_pressure"] = ""
    else:
        normalized["blood_pressure"] = ""
    # Se il contesto è "Checkup", azzera tutti i campi tranne quelli specificati
    if usage_mode == "Checkup":
        fields_to_keep = {
            "first_name", "last_name", "medications_taken",
            "heart_rate", "oxygenation", "blood_pressure",
            "temperature", "blood_glucose", "medical_actions",
            "assessment", "plan", "symptoms"
        }
        for key in list(normalized.keys()):
            if key not in fields_to_keep:
                normalized[key] = ""
    return normalized

def validate_fields(data, file_content):
    error_fields = []
    original_text_lower = file_content.lower()

    # Verifica nome
    try:
        first_name_raw = data.get("first_name")
        if first_name_raw and str(first_name_raw).strip() != "":
            name_value = str(first_name_raw).strip()
            if len(name_value) < 2 or name_value.lower() not in original_text_lower:
                error_fields.append("first_name")
    except:
        pass

    # Verifica cognome
    try:
        last_name_raw = data.get("last_name")
        if last_name_raw and str(last_name_raw).strip() != "":
            surname_value = str(last_name_raw).strip()
            if len(surname_value) < 2 or surname_value.lower() not in original_text_lower:
                error_fields.append("last_name")
    except:
        pass

    # Verifica città di residenza
    try:
        city_raw = data.get("residence_city")
        if city_raw and str(city_raw).strip() != "":
            city = str(city_raw).strip()
            if len(city) < 2 or city.lower() not in original_text_lower:
                error_fields.append("residence_city")
    except:
        pass

    # Verifica indirizzo di residenza
    try:
        address_raw = data.get("residence_address")
        if address_raw and str(address_raw).strip() != "":
            address = str(address_raw).strip()
            if len(address) < 5 or address.lower() not in original_text_lower:
                error_fields.append("residence_address")
    except:
        pass

    # Verifica numero di telefono
    try:
        phone_raw = data.get("phone")
        if phone_raw and str(phone_raw).strip() != "":
            phone = str(phone_raw).strip()
            phone_digits = re.sub(r"\D", "", phone)
            text_digits = re.sub(r"\D", "", file_content)
            if len(phone_digits) < 6 or phone_digits not in text_digits:
                error_fields.append("phone")
    except:
        pass

    # Verifica dell'età
    age_value = None
    try:
        age_raw = data.get("age")
        if age_raw and str(age_raw).strip() != "":
            age_str = str(age_raw).strip()
            match = re.search(r"\d+", age_str)
            if match:
                age_value = int(match.group())
                if not (0 <= age_value <= 130) or str(age_value) not in file_content:
                    error_fields.append("age")
            else:
                error_fields.append("age")
    except:
        pass

    # Verifica anno di nascita
    birth_year = None
    try:
        birth_date_raw = data.get("birth_date")
        if birth_date_raw and str(birth_date_raw).strip() != "":
            bd_str = str(birth_date_raw).strip()

            # Cerca un numero di 4 cifre (es. "1984")
            year_match = re.search(r"\b(19|20)\d{2}\b", bd_str)
            if year_match:
                birth_year = int(year_match.group(0))
            else:
                # Prova a fare il parsing della data se non ha solo l'anno
                bd = parse(bd_str, dayfirst=True, fuzzy=True)
                birth_year = bd.year

            if str(birth_year) not in file_content:
                error_fields.append("birth_date")
    except Exception:
        pass

    # Check coerenza età - anno di nascita
    try:
        current_year = datetime.now().year
        if birth_year is not None and age_value is not None:
            expected_year = current_year - age_value
            if abs(birth_year - expected_year) > 1 and "age" not in error_fields and "birth_date" not in error_fields:
                error_fields.append("age")
                error_fields.append("birth_date")
    except:
        pass

    # Verifica temperatura
    try:
        temp_raw = data.get("temperature")
        if temp_raw and str(temp_raw).strip() != "":
            temp_str = str(temp_raw).strip()
            temp_match = re.search(r"([-+]?\d+(\.\d+)?)", temp_str)
            if temp_match:
                temp_value = float(temp_match.group(1))
                if not (0 <= temp_value <= 50) or str(int(temp_value)) not in file_content:
                    error_fields.append("temperature")
            else:
                error_fields.append("temperature")
    except:
        pass

    # Verifica ossigenazione
    try:
        oxy_raw = data.get("oxygenation")
        if oxy_raw and str(oxy_raw).strip() != "":
            oxy_str = str(oxy_raw).strip()
            oxy_match = re.search(r"(\d{1,3})", oxy_str)
            if oxy_match:
                oxy_value = int(oxy_match.group(1))
                if oxy_value > 100 or str(oxy_value) not in file_content:
                    error_fields.append("oxygenation")
            else:
                error_fields.append("oxygenation")
    except:
        pass

    # Frequenza cardiaca
    try:
        heart_rate_raw = data.get("heart_rate")
        if heart_rate_raw and str(heart_rate_raw).strip() != "":
            bpm_str = str(heart_rate_raw).strip()
            bpm_match = re.search(r"(\d{2,3})", bpm_str)
            if bpm_match:
                bpm_value = int(bpm_match.group(1))
                if not (0 <= bpm_value <= 700) or str(bpm_value) not in file_content:
                    error_fields.append("heart_rate")
            else:
                error_fields.append("heart_rate")
    except:
        pass

    # Glicemia
    try:
        glucose_raw = data.get("blood_glucose")
        if glucose_raw and str(glucose_raw).strip() != "":
            glu_str = str(glucose_raw).strip()
            glu_match = re.search(r"\d{2,3}", glu_str)
            if glu_match:
                glu_value = int(glu_match.group())
                if glu_value < 20 or glu_value > 500 or str(glu_value) not in file_content:
                    error_fields.append("blood_glucose")
            else:
                error_fields.append("blood_glucose")
    except:
        pass

    return list(set(error_fields))
    

def extract_all(text):
    prompt = f"""Extract the required information in JSON format from the following clinical text:
    {text}
    ----
    Requirements:
    - Translate fields and values into the same language as the input.
    - Keep the JSON compact.
    - For fields that are not explicitly mentioned in the text, return an empty string "".

    required information:
        - first_name: name of patient
        - last_name:
        - access_mode: Specify how the patient arrived
        - birth_date:
        - birth_place:
        - age:
        - gender: 
        - residence_city:
        - residence_address: 
        - phone:
        - skin_state:
        - consciousness_state:
        - pupils_state:
        - respiratory_state:
        - history:
        - medications_taken:
        - symptoms:
        - heart_rate:
        - oxygenation:
        - blood_pressure:
        - temperature:
        - blood_glucose:
        - medical_actions:
        - assessment:
        - plan:
        - triage_code: 

    JSON:
    """

    # Tokenizza input + genera output
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
    )

    # Decodifica risposta
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

def extract_json_block(text):
    start = text.find('{')
    if start == -1:
        return None

    depth = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start:i+1]  # JSON completo
    return None  # JSON non chiuso correttamente

def parse_generated_json(generated_text: str):
    """
    Cerca e analizza un blocco JSON all'interno del testo generato dal modello.

    Args:
        generated_text (str): Il testo completo generato dal modello, contenente un blocco JSON.

    Returns:
        dict | None: Il dizionario Python se il parsing ha successo, altrimenti None.
    """
    json_str = extract_json_block(generated_text)

    if json_str:
        try:
            patient_info = json.loads(json_str)
            print("✅ JSON estratto e parsato:")
            return patient_info
        except json.JSONDecodeError as e:
            print("❌ Errore nel parsing JSON:", e)
            print("📄 Testo JSON grezzo:")
            return None
    else:
        print("⚠️ Nessun JSON trovato nella risposta generata:")
        return None


