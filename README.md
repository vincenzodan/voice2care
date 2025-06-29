
# 🩺 Voice2Care
Voice2Care è un progetto che mira a semplificare la digitalizzazione dei dati clinici attraverso la trascrizione automatica di registrazioni audio e l’estrazione delle informazioni rilevanti in formato strutturato. 
Nasce dall’esigenza di rendere la registrazione delle informazioni rapida ed efficiente in ambienti ad alta intensità, come il pronto soccorso o il pronto intervento, dove la velocità di azione è fondamentale.

## 📘 Documentazione Tecnica
Consulta la [documentazione tecnica](./Documentazione.pdf) per ulteriori dettagli sul funzionamento del progetto.

---
## 📖 Istruzioni per l'Esecuzione

### 💻 Esecuzione Locale

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
   streamlit run script/dashboard1.py
   ```

3. **Avvio della seconda dashboard**:
   ```bash
   streamlit run script/dashboard2.py
   ```

### 🖥️ Esecuzione su Kaggle

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

## 🗂️ Struttura del Progetto

```
voice2care/
│
├── dataset/                     # Dati di input (audio, file, ecc.)
├── script/
│   ├── voice2care.ipynb         # Notebook per l'esecuzione su Kaggle
│   ├── testing.ipynb            # Notebook per test
│   ├── dashboard1.py            # Prima dashboard Streamlit
│   ├── dashboard2.py            # Seconda dashboard Streamlit
│   ├── transcription.py         # Modulo per trascrizione audio
│   ├── extraction.py            # Modulo per estrazione dati
│   ├── db.py                    # Modulo per interazione con il database MongoDB
│   ├── report.py                # Modulo per la generazione del report PDF
│   ├── config.py                # File di configurazione (token, chiavi API, ecc.)
│   └── assets/                  # Risorse aggiuntive (immagini, loghi, ecc.)
├── working/                     # Cartella per output testing
├── requirements.txt             # Elenco delle dipendenze Python necessarie
├── Documentazione.pdf           # Documentazione completa del progetto
└── README.md                    # Istruzioni per installazione e uso del progetto

```

---

## 👥 Contributors

- [@Vincenzo D'Angelo](https://github.com/vincenzodan)
- [@Giorgio Di Costanzo](https://github.com/GiorgioDiCostanzo)
