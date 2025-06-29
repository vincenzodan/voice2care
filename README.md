
# 🗣️ Voice2Care – Istruzioni per l'Esecuzione

## 📘 Documentazione Tecnica
Consulta la [documentazione tecnica](./Documentazione.pdf) per ulteriori dettagli sul funzionamento del progetto.

---

## ✅ Esecuzione Locale

1. **Installare i requisiti** dal file `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

   🔹 *Nota: i pacchetti `openai-whisper` e `sentencepiece` potrebbero richiedere installazione separata:*
   ```bash
   pip install openai-whisper sentencepiece
   ```

2. **Avvio della prima dashboard**:
   ```bash
   streamlit run ./voice2care/script/dashboard1.py
   ```

3. **Avvio della seconda dashboard**:
   ```bash
   streamlit run ./voice2care/script/dashboard2.py
   ```

---

## 🧪 Esecuzione su Kaggle

1. Registrarsi su [Kaggle](https://www.kaggle.com) e verificare l’account con il numero di telefono per abilitare le GPU.
2. Caricare il notebook su Kaggle.
3. Caricare tutto il codice come *Dataset esterno*.
4. Impostare il path del file `app.py` nell’ultima cella del notebook.
5. Impostare il path del file `config.py` nella cella dedicata a Ngrok.
6. Avviare tutte le celle del notebook.
7. Quando lo streamlit è attivo, accedere al link fornito da Ngrok nella cella precedente.

   💡 *Puoi eseguire contemporaneamente la seconda dashboard in locale con:*
   ```bash
   streamlit run ./voice2care/script/dashboard2.py
   ```

---

## 🧾 Struttura del Progetto

```
voice2care/
│
├── script/
│   ├── app.py                   # Prima dashboard
│   ├── dashboard_hospital.py    # Seconda dashboard
│   ├── config.py                # Configurazioni Ngrok e API
│   ├── report.py                # Generazione report PDF (con ReportLab)
│   └── ...
├── dataset/                     # Dati di input
├── requirements.txt             # Dipendenze del progetto
└── README.md                    # Questo file
```

## 👥 Contributors

- [@vincenzodan](https://github.com/vincenzodan)
- [@GiorgioDiCostanzo](https://github.com/GiorgioDiCostanzo)
