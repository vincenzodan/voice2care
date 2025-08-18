![gemma-color](https://github.com/user-attachments/assets/1be74599-7f8a-4a50-9fd6-0075a5df6eed)
# 🩺 Voice2Care
Voice2Care è un progetto che mira a semplificare la digitalizzazione dei dati clinici attraverso la trascrizione automatica di registrazioni audio e l’estrazione delle informazioni rilevanti in formato strutturato. 
Nasce dall’esigenza di rendere la registrazione delle informazioni rapida ed efficiente in ambienti ad alta intensità, come il pronto soccorso o il pronto intervento, dove la velocità di azione è fondamentale.

## 📘 Documentazione Tecnica
Consulta la [documentazione tecnica](./Documentazione.pdf) per ulteriori dettagli sul funzionamento del progetto.

---
## 🛠️ Technologies

<table>
  <tr>
    <td align="center">
      <a href="https://www.python.org/" target="_blank">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="50" height="50"/><br>
        Python
      </a>
    </td>
    <td align="center">
      <a href="https://www.mongodb.com/" target="_blank">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original.svg" width="50" height="50"/><br>
        MongoDB
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/openai/whisper" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/OpenAI_Logo.svg" width="50" height="50"/><br>
        Whisper
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/cs230-stanford/Gemma" target="_blank">
        <img src=[<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>Gemma</title><defs><linearGradient id="lobe-icons-gemma-fill" x1="24.419%" x2="75.194%" y1="75.581%" y2="25.194%"><stop offset="0%" stop-color="#446EFF"></stop><stop offset="36.661%" stop-color="#2E96FF"></stop><stop offset="83.221%" stop-color="#B1C5FF"></stop></linearGradient></defs><path d="M12.34 5.953a8.233 8.233 0 01-.247-1.125V3.72a8.25 8.25 0 015.562 2.232H12.34zm-.69 0c.113-.373.199-.755.257-1.145V3.72a8.25 8.25 0 00-5.562 2.232h5.304zm-5.433.187h5.373a7.98 7.98 0 01-.267.696 8.41 8.41 0 01-1.76 2.65L6.216 6.14zm-.264-.187H2.977v.187h2.915a8.436 8.436 0 00-2.357 5.767H0v.186h3.535a8.436 8.436 0 002.357 5.767H2.977v.186h2.976v2.977h.187v-2.915a8.436 8.436 0 005.767 2.357V24h.186v-3.535a8.436 8.436 0 005.767-2.357v2.915h.186v-2.977h2.977v-.186h-2.915a8.436 8.436 0 002.357-5.767H24v-.186h-3.535a8.436 8.436 0 00-2.357-5.767h2.915v-.187h-2.977V2.977h-.186v2.915a8.436 8.436 0 00-5.767-2.357V0h-.186v3.535A8.436 8.436 0 006.14 5.892V2.977h-.187v2.976zm6.14 14.326a8.25 8.25 0 005.562-2.233H12.34c-.108.367-.19.743-.247 1.126v1.107zm-.186-1.087a8.015 8.015 0 00-.258-1.146H6.345a8.25 8.25 0 005.562 2.233v-1.087zm-8.186-7.285h1.107a8.23 8.23 0 001.125-.247V6.345a8.25 8.25 0 00-2.232 5.562zm1.087.186H3.72a8.25 8.25 0 002.232 5.562v-5.304a8.012 8.012 0 00-1.145-.258zm15.47-.186a8.25 8.25 0 00-2.232-5.562v5.315c.367.108.743.19 1.126.247h1.107zm-1.086.186c-.39.058-.772.144-1.146.258v5.304a8.25 8.25 0 002.233-5.562h-1.087zm-1.332 5.69V12.41a7.97 7.97 0 00-.696.267 8.409 8.409 0 00-2.65 1.76l3.346 3.346zm0-6.18v-5.45l-.012-.013h-5.451c.076.235.162.468.26.696a8.698 8.698 0 001.819 2.688 8.698 8.698 0 002.688 1.82c.228.097.46.183.696.259zM6.14 17.848V12.41c.235.078.468.167.696.267a8.403 8.403 0 012.688 1.799 8.404 8.404 0 011.799 2.688c.1.228.19.46.267.696H6.152l-.012-.012zm0-6.245V6.326l3.29 3.29a8.716 8.716 0 01-2.594 1.728 8.14 8.14 0 01-.696.259zm6.257 6.257h5.277l-3.29-3.29a8.716 8.716 0 00-1.728 2.594 8.135 8.135 0 00-.259.696zm-2.347-7.81a9.435 9.435 0 01-2.88 1.96 9.14 9.14 0 012.88 1.94 9.14 9.14 0 011.94 2.88 9.435 9.435 0 011.96-2.88 9.14 9.14 0 012.88-1.94 9.435 9.435 0 01-2.88-1.96 9.434 9.434 0 01-1.96-2.88 9.14 9.14 0 01-1.94 2.88z" fill="url(#lobe-icons-gemma-fill)" fill-rule="evenodd"></path></svg>Uploading gemma-color.svg…]()

        Gemma
      </a>
    </td>
  </tr>
</table>

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
2. Caricare il notebook su Kaggle (per evitare errori andare in Advanced Setting: Version Type -> Quick Save).
3. Caricare tutto il codice come *Dataset esterno*.
4. Impostare il path del file `dashboard1.py` nell’ultima cella del notebook.
5. Impostare il path del file `config.py` nella cella dedicata a Ngrok.
6. Avviare tutte le celle del notebook.
7. Quando lo streamlit è attivo, accedere al link fornito da Ngrok nella cella precedente.

   💡 *Puoi eseguire contemporaneamente la seconda dashboard in locale con:*
   ```bash
   streamlit run script/dashboard2.py
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
