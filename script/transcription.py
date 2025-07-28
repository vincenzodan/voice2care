import whisper
import librosa
import re

model = whisper.load_model("medium")

def transcribe_audio(file_path):

    audio, sr = librosa.load(file_path, sr=16000, mono=True)
    result = model.transcribe(audio)
    text = result["text"]

    # Regex per maggiore flessibilità 
    text = re.sub(r"\bmilligrams?\s+per\s+deciliter\b", "mg/dl", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmilligrammi?\s+per\s+decilitro\b", "mg/dl", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmg?\s+per\s+decilitro\b", "mg/dl", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmillimeters?\s+of\s+mercury\b", "mmHg", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmillimetri?\s+di\s+merc[ur]io\b", "mmHg", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmm?\s+di\s+merc[ur]io\b", "mmHg", text, flags=re.IGNORECASE)

    text = re.sub(r"\b(\d+)\s+over\s+(\d+)\b", r"\1/\2", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(\d+)\s+su\s+(\d+)\b", r"\1/\2", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(\d+)\s+slash\s+(\d+)\b", r"\1/\2", text, flags=re.IGNORECASE)

    text = re.sub(r"\bbeats?\s+per\s+minute\b", "bpm", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbattiti?\s+al\s+minuto\b", "bpm", text, flags=re.IGNORECASE)

    text = re.sub(r"\bdegrees?\s+celsius\b", "°C", text, flags=re.IGNORECASE)
    text = re.sub(r"\bgradi?\s+celsius\b", "°C", text, flags=re.IGNORECASE)

    text = re.sub(r"\b(\d+)\s+percent\b", r"\1%", text, flags=re.IGNORECASE)
    text = re.sub(r"\bper\s+cento\b", "%", text, flags=re.IGNORECASE)


    return text.strip()

