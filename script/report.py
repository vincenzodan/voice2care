from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import json
import os

def generate_pdf_report(data, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    margin_x = 50
    margin_y = 50
    right_margin = width - 50
    line_height = 16
    y = height - margin_y

    ########## INTESTAZIONE

    lines = [
        "USL FUORIGROTTA - Azienda Sanitaria",
        "Nuovo ospedale di Fuorigrotta S. Diego Armando",
        "Unità operativa Medicina d'Urgenza Pronto Soccorso",
        "Responsabile Dott. Antonio Conte"
    ]

    lines2 = [
        "PRONTO SOCCORSO",
        "___________________________",
        "                           ",
    ]
    # Punto di partenza verticale   
    y = 750  

    # Parametri box
    box_width = 200
    box_height = 100
    box_x = width - box_width  # 50px di margine dal bordo destro
    box_y = height - box_height -40  # 50px dal bordo superiore

    # Testo di base
    lines0 = [
        "Sede Legale",
        "A.O.R.N. D.Armando",
        "Via Claudio, 21",
        "80125 NAPOLI",
        "1234567890123456"
    ]

    # Stile testo
    font_name = "Helvetica"
    font_size = 8
    line_spacing = 10

    # Imposta il font
    c.setFont(font_name, font_size)

    # Calcola posizione di partenza per la prima riga (centrata verticalmente)
    start_y = box_y + box_height - line_spacing 

    for line in lines0:
        text_width = c.stringWidth(line, font_name, font_size)
        x_position = box_x + (box_width - text_width) / 2
        c.drawString(x_position, start_y, line)
        start_y -= line_spacing  # va alla riga successiva

    #c.drawImage("logo2.jpg", 120, height - 50 - 40, width=50, height=50)
    # Parametri del logo
    logo_x = 80
    logo_y = height - 40 - 40
    logo_width = 50
    logo_height = 50

    # Disegna il logo
    base_dir = os.path.dirname(__file__)  # cartella dello script
    logo_path = os.path.join(base_dir, "assets", "logo2.jpg")

    c.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height)

    # Testo sotto il logo, centrato rispetto all'immagine
    center_x = logo_x + logo_width / 2
    text_start_y = logo_y - 4  # distanza dal basso dell'immagine

    # Riga 1 - Titolo (grassetto)
    c.setFont("Helvetica-Bold", 9)
    text = "S. Diego Armando"
    text_width = c.stringWidth(text, "Helvetica-Bold", 9)
    c.drawString(center_x - text_width / 2, text_start_y, text)

    # Riga 2 - Sottotitolo 1
    c.setFont("Helvetica", 6)
    text2 = "AZIENDA OSPEDALIERA"
    text_width2 = c.stringWidth(text2, "Helvetica", 6)
    c.drawString(center_x - text_width2 / 2, text_start_y - 8, text2)

    # Riga 3 - Sottotitolo 2
    text3 = "DI RILIEVO NAZIONALE"
    text_width3 = c.stringWidth(text3, "Helvetica", 6)
    c.drawString(center_x - text_width3 / 2, text_start_y - 16, text3)


    # Prima lista, font normale
    c.setFont("Helvetica", 9)

    for line in lines:
        text_width = c.stringWidth(line, "Helvetica", 9)
        x_position = (width - text_width) / 2
        c.drawString(x_position, y, line)
        y -= 12  # scendi di 12 punti per la riga successiva

    # Seconda lista, font grassetto
    c.setFont("Helvetica-Bold", 9)

    for line in lines2:
        text_width = c.stringWidth(line, "Helvetica-Bold", 9)
        x_position = (width - text_width) / 2
        c.drawString(x_position, y, line)
        y -= 12

    c.setFont("Helvetica-Bold", 11)
    text_width = c.stringWidth("RELAZIONE CLINICA", "Helvetica-Bold", 11)
    x_position = (width - text_width) / 2
    c.drawString(x_position, y, "RELAZIONE CLINICA")

    triage_date = " ".join(data.get("triage_date", [""])) or ""
    try:
        triage_date_obj = datetime.strptime(triage_date, "%d/%m/%Y %H:%M")
        formatted_date = triage_date_obj.strftime("%d/%m/%Y")
    except ValueError:
        formatted_date = ""

    ID = (data.get("ID") or [""])[0]

    c.setFont("Helvetica", 9)
    c.drawString(50, y-12, f"Fuorigrotta, lì: {formatted_date}")
    c.setFont("Helvetica-Bold", 9)
    x_right = right_margin - text_width
    c.drawString(x_right, y-12, f"N.VERBALE: {ID}")
    
        # === BOX DATI ANAGRAFICI ASSISTITO ===
    box_x = margin_x
    box_y = y - 90  # distanza verticale da dove eravamo rimasti
    box_width = width - 2 * margin_x
    box_height = 64

    # Colonne per allineamento
    col1 = box_x + 10
    col2 = box_x + box_width / 3 +20
    col3 = box_x + 2 * box_width / 3
    

    c.rect(box_x, box_y, box_width, box_height, stroke=1)

    # Imposta font
    font_size = 10
    c.setFont("Helvetica", font_size)
    text_y = box_y + box_height - 14  # prima riga dentro il box

    def safe_get(data, key):
        value = data.get(key, "")
        if isinstance(value, list):
            return str(value[0]) if value else ""
        return str(value)

    # Estrai i dati dal JSON
    nome = safe_get(data, "first_name")
    cognome = safe_get(data, "last_name")
    sesso_raw = safe_get(data, "gender")
    sesso = "F" if sesso_raw and sesso_raw[0].lower().startswith("f") else ("M" if sesso_raw else "")
    residence_city = safe_get(data, "residence_city")
    eta = safe_get(data, "age")
    data_nascita = safe_get(data, "birth_date")
    indirizzo = safe_get(data, "residence_address")
    telefono = safe_get(data, "phone")
    birth_place = safe_get(data, "birth_place")
    sintomi = safe_get(data, "symptoms")
    access_mode = safe_get(data, "access_mode")
    assessment = safe_get(data, "assessment")
    plan = safe_get(data, "plan")

    # Riga 1: Assistito/a | Sesso | Età
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col1, text_y, "Assistito/a")
    c.setFont("Helvetica", font_size)
    c.drawString(col1 + 70, text_y, f"{cognome} {nome}")

    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col2, text_y, "Sesso")
    c.setFont("Helvetica", font_size)
    c.drawString(col2 + 60, text_y, sesso)

    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col3, text_y, "Età")
    c.setFont("Helvetica", font_size)
    c.drawString(col3 + 25, text_y, eta)

    text_y -= 14

    # Riga 2: Data e luogo di nascita
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col1, text_y, "Nato/a il")
    c.setFont("Helvetica", font_size)
    c.drawString(col1 + 70, text_y, data_nascita)
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col2, text_y, "a")
    c.setFont("Helvetica", font_size)
    c.drawString(col2 + 60, text_y, birth_place)

    text_y -= 14

    # Riga 3: Residenza e Indirizzo
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col1, text_y, "Residenza")
    c.setFont("Helvetica", font_size)
    c.drawString(col1 + 70, text_y, residence_city)

    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col2, text_y, "Indirizzo")
    c.setFont("Helvetica", font_size)
    c.drawString(col2 + 60, text_y, indirizzo)

    text_y -= 14

    # Riga 4: Telefono
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col1, text_y, "Telefono")
    c.setFont("Helvetica", font_size)
    c.drawString(col1 + 70, text_y, telefono)

    # Aggiorna y per il contenuto successivo
    y = box_y - 20
    
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col1, y, "Motivo Accesso:")
    c.setFont("Helvetica", font_size)
    c.drawString(col1 + 100, y, sintomi)

    c.setFont("Helvetica-Bold", font_size)
    c.drawString(col1, y-12, "Modalità Accesso:")
    c.setFont("Helvetica", font_size)
    c.drawString(col1 + 100, y-12, access_mode)

    # === Box DATE E URGENZE ===
    box2_x = 50
    box2_y = y - 80  # y attuale meno un po’ di spazio
    box2_width = width - 2 * margin_x
    box2_height = 35

    # Disegna il bordo del box
    c.rect(box2_x, box2_y, box2_width, box2_height)

    # Imposta font
    label_font = "Helvetica-Bold"
    value_font = "Helvetica"
    font_size = 10
    c.setFont(label_font, font_size)

    # Dati di esempio (recupera questi da data o setta a "")
    data_triage = (data.get("triage_date") or [""])[0]
    data_visita = (data.get("visit_date") or [""])[0]
    data_uscita = (data.get("exit_date") or [""])[0]
    urgenza_triage = safe_get(data, "triage_code")
    urgenza_dimissione = safe_get(data, "discharge_code")

    # Coordinate di partenza per testo (3 colonne per riga)
    col1 = box2_x + 10
    col2 = box2_x + box2_width / 3
    col3 = box2_x + 2 * box2_width / 3
    row1_y = box2_y + box2_height - 15
    row2_y = row1_y - 12

    # RIGA 1
    c.drawString(col1, row1_y, "Data triage:")
    c.setFont(value_font, font_size)
    c.drawString(col1 + 70, row1_y, data_triage)

    c.setFont(label_font, font_size)
    c.drawString(col2, row1_y, "Data visita:")
    c.setFont(value_font, font_size)
    c.drawString(col2 + 65, row1_y, data_visita)

    c.setFont(label_font, font_size)
    c.drawString(col3, row1_y, "Data uscita:")
    c.setFont(value_font, font_size)
    c.drawString(col3 + 65, row1_y, data_uscita)

    # RIGA 2
    c.setFont(label_font, font_size)
    c.drawString(col1, row2_y, "Urgenza triage:")
    c.setFont(value_font, font_size)
    c.drawString(col1 + 85, row2_y, urgenza_triage)

    c.setFont(label_font, font_size)
    c.drawString(col3, row2_y, "Urgenza dimissione:")
    c.setFont(value_font, font_size)
    c.drawString(col3 + 65, row2_y, urgenza_dimissione)

    # Aggiornamento di y
    y = box2_y - 20

    history = safe_get(data, "history")
    medications_taken = safe_get(data, "medications_taken")
    consciousness_state = safe_get(data, "consciousness_state")
    respiratory_state = safe_get(data, "respiratory_state")
    skin_state = safe_get(data, "skin_state")
    pupils_state = safe_get(data, "pupils_state")
    annotations = safe_get(data, "annotations")
    medical_actions = safe_get(data, "medical_actions")

    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Anamnesi:")
    c.setFont(value_font, font_size)
    y = y-12
    c.drawString(150, y, history)
    y = y-12
    c.drawString(150, y, medications_taken)
    y -= 24

    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Rilevazioni:")
    c.setFont("Helvetica-Bold", font_size)
    y -= 12

    font_size = 10

    c.setFont(value_font, font_size)
    c.drawString(150, y, "- coscienza:")
    c.drawString(250, y, consciousness_state)
    y -= 12

    c.drawString(150, y, "- pupille:")
    c.setFont(value_font, font_size)
    c.drawString(250, y, pupils_state)
    y -= 12

    c.drawString(150, y, "- respiro:")
    c.setFont(value_font, font_size)
    c.drawString(250, y, respiratory_state)
    y -= 12

    c.drawString(150, y, "- cute:")
    c.setFont(value_font, font_size)
    c.drawString(250, y, skin_state)
    y -= 24

    table_data = [
    ["SpO2", "FC (bpm)", "Temp (°C)", "Glic (Mg/dl)", "PA (mmHg)"],
    [
        safe_get(data, "oxygenation"),
        safe_get(data, "heart_rate"),
        safe_get(data, "temperature"),
        safe_get(data, "blood_glucose"),
        safe_get(data, "blood_pressure")
    ]
    ]

    # Calcola larghezze colonna dinamiche
    available_width = width - 2 * margin_x
    num_columns = len(table_data[0])
    col_widths = [available_width / num_columns] * num_columns

    # Crea la tabella
    table = Table(table_data, colWidths=col_widths)

    # Stile della tabella
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Disegna la tabella
    table.wrapOn(c, width, height)
    table.drawOn(c, margin_x, y - 40)

    y -= 40  # Abbassa il cursore per il contenuto successivo

    y = y - 24

    c.setFont("Helvetica", font_size)
    c.drawString(50, y, medical_actions)

    y-=24
    
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Valutazione:")
    c.setFont("Helvetica", font_size)
    y = y-12
    c.drawString(150, y, assessment)

    y = y - 24
    
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Piano:")
    y =y-12
    c.setFont("Helvetica", font_size)
    c.drawString(150, y, plan)

    y -= 24

    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Note e Prescrizioni:")
    c.setFont("Helvetica", font_size)
    y -= 12

    c.drawString(150, y, annotations)

    footer_y = 80  # distanza dal fondo del foglio

    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, footer_y + 35, "Dichiara di aver preso visione di quanto sopra, e di essere stato informato in modo comprensibile sulle proprie")
    c.drawString(50, footer_y + 25, "condizioni di salute, sulla terapia proposta e sui rischi connessi")

    # Etichette firme equidistanti
    sign_labels = ["Firma dell'accompagnatore", "Firma del paziente", "Il medico dimettente"]
    positions = [width * 0.2, width * 0.5, width * 0.8]

    c.setFont("Helvetica", 9)
    for text, x in zip(sign_labels, positions):
        c.drawCentredString(x, footer_y, text)

    # Linee firma sotto
    signature_lines = ["_________________________", "_________________________", "_________________________"]
    for line, x in zip(signature_lines, positions):
        c.drawCentredString(x, footer_y - 20, line)

    c.save()

def generate_pdf_checkup(data, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    margin_x = 50
    margin_y = 50
    right_margin = width - 50
    line_height = 16
    y = height - margin_y

    ########## INTESTAZIONE

    lines = [
        "USL FUORIGROTTA - Azienda Sanitaria",
        "Nuovo ospedale di Fuorigrotta S. Diego Armando",
        "Unità operativa Medicina d'Urgenza Pronto Soccorso",
        "Responsabile Dott. Antonio Conte"
    ]

    lines2 = [
        "PRONTO SOCCORSO",
        "___________________________",
        "                           ",
    ]

    y = 750  # Punto di partenza verticale

    # Parametri box
    box_width = 200
    box_height = 100
    box_x = width - box_width  # 50px di margine dal bordo destro
    box_y = height - box_height -40  # 50px dal bordo superiore

    # Testo da inserire
    lines0 = [
        "Sede Legale",
        "A.O.R.N. D.Armando",
        "Via Claudio, 21",
        "80125 NAPOLI",
        "1234567890123456"
    ]

    # Stile testo
    font_name = "Helvetica"
    font_size = 8
    line_spacing = 10

    # Imposta il font
    c.setFont(font_name, font_size)

    # Calcola posizione di partenza per la prima riga (centrata verticalmente)
    start_y = box_y + box_height - line_spacing  # prima riga un po' sotto il top

    for line in lines0:
        text_width = c.stringWidth(line, font_name, font_size)
        x_position = box_x + (box_width - text_width) / 2
        c.drawString(x_position, start_y, line)
        start_y -= line_spacing  # vai alla riga successiva

    #c.drawImage("logo2.jpg", 120, height - 50 - 40, width=50, height=50)
    # Parametri del logo
    logo_x = 80
    logo_y = height - 40 - 40
    logo_width = 50
    logo_height = 50

    # Disegna il logo
    base_dir = os.path.dirname(__file__)  # cartella dello script
    logo_path = os.path.join(base_dir, "assets", "logo2.jpg")

    c.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height)

    # Testo sotto il logo, centrato rispetto all'immagine
    center_x = logo_x + logo_width / 2
    text_start_y = logo_y - 4  # distanza dal basso dell'immagine

    # Riga 1 - Titolo (grassetto)
    c.setFont("Helvetica-Bold", 9)
    text = "S. Diego Armando"
    text_width = c.stringWidth(text, "Helvetica-Bold", 9)
    c.drawString(center_x - text_width / 2, text_start_y, text)

    # Riga 2 - Sottotitolo 1
    c.setFont("Helvetica", 6)
    text2 = "AZIENDA OSPEDALIERA"
    text_width2 = c.stringWidth(text2, "Helvetica", 6)
    c.drawString(center_x - text_width2 / 2, text_start_y - 8, text2)

    # Riga 3 - Sottotitolo 2
    text3 = "DI RILIEVO NAZIONALE"
    text_width3 = c.stringWidth(text3, "Helvetica", 6)
    c.drawString(center_x - text_width3 / 2, text_start_y - 16, text3)


    # Prima lista, font normale
    c.setFont("Helvetica", 9)

    for line in lines:
        text_width = c.stringWidth(line, "Helvetica", 9)
        x_position = (width - text_width) / 2
        c.drawString(x_position, y, line)
        y -= 12  # scendi di 12 punti per la riga successiva

    # Seconda lista, font grassetto
    c.setFont("Helvetica-Bold", 9)

    for line in lines2:
        text_width = c.stringWidth(line, "Helvetica-Bold", 9)
        x_position = (width - text_width) / 2
        c.drawString(x_position, y, line)
        y -= 12

    c.setFont("Helvetica-Bold", 11)
    text_width = c.stringWidth("MONITORAGGIO GIORNALIERO", "Helvetica-Bold", 11)
    x_position = (width - text_width) / 2
    c.drawString(x_position, y, "MONITORAGGIO GIORNALIERO")

    data_checkup = datetime.now().strftime("%d/%m/%Y %H:%M")

    ID = (data.get("ID") or [""])[0]

    c.setFont("Helvetica", 9)
    c.setFont("Helvetica-Bold", 9)
    x_right = right_margin - text_width
    
        # === BOX DATI ANAGRAFICI ASSISTITO ===
    box_x = margin_x
    box_y = y - 110  # distanza verticale da dove eravamo rimasti
    box_width = width - 2 * margin_x
    box_height = 90

    # Colonne per allineamento
    col1 = box_x + 5
    col2 = box_x + box_width / 2
    col3 = box_x + box_width - 150

    # Imposta font
    font_size = 10
    c.setFont("Helvetica", font_size)

    def safe_get(data, key):
        value = data.get(key, "")
        if isinstance(value, list):
            return str(value[0]) if value else ""
        return str(value)

    # Estrai i dati dal JSON
    nome = safe_get(data, "first_name")
    cognome = safe_get(data, "last_name")
    sintomi = safe_get(data, "symptoms")
    assessment = safe_get(data, "assessment")
    plan = safe_get(data, "plan")
    medical_actions = safe_get(data, "medical_actions")
    
    y = y-24

    c.drawString(50, y, f"Data visita: {data_checkup}")

    y = y - 24

    # Riga 1: Assistito/a 
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Assistito/a")
    c.setFont("Helvetica", font_size)
    c.drawString(150, y, f"{cognome} {nome}")

    y = y - 24
    
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Sintomi:")
    c.setFont("Helvetica", font_size)
    c.drawString(150, y, sintomi)

    y = y - 24

    value_font = "Helvetica"
    medications_taken = safe_get(data, "medications_taken")

    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Terapia in corso:")
    c.setFont(value_font, font_size)
    c.drawString(150, y, medications_taken)
    y -= 24

    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Rilevazioni:")
    c.setFont("Helvetica-Bold", font_size)
    y -= 12

    table_data = [
    ["SpO2", "FC (bpm)", "Temp (°C)", "Glic (Mg/dl)", "PA (mmHg)"],
    [
        safe_get(data, "oxygenation"),
        safe_get(data, "heart_rate"),
        safe_get(data, "temperature"),
        safe_get(data, "blood_glucose"),
        safe_get(data, "blood_pressure")
    ]
    ]

    # Calcola larghezze colonna dinamiche
    available_width = width - 2 * margin_x
    num_columns = len(table_data[0])
    col_widths = [available_width / num_columns] * num_columns

    # Crea la tabella
    table = Table(table_data, colWidths=col_widths)

    # Stile della tabella
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Disegna la tabella
    table.wrapOn(c, width, height)
    table.drawOn(c, margin_x, y - 40)
    y -= 40  # Abbassa il cursore per il contenuto successivo

    y = y - 24

    c.setFont("Helvetica", font_size)
    c.drawString(50, y, medical_actions)

    y = y - 24
    
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Valutazione:")
    c.setFont("Helvetica", font_size)
    c.drawString(150, y, assessment)

    y = y - 24
    
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(50, y, "Piano:")
    c.setFont("Helvetica", font_size)
    c.drawString(150, y, plan)

    footer_y = 80  # distanza dal fondo del foglio

    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, footer_y + 35, "Dichiara di aver preso visione di quanto sopra, e di essere stato informato in modo comprensibile sulle proprie")
    c.drawString(50, footer_y + 25, "condizioni di salute, sulla terapia proposta e sui rischi connessi")

    # Etichette firme equidistanti
    sign_labels = ["Firma dell'accompagnatore", "Firma del paziente", "Il medico dimettente"]
    positions = [width * 0.2, width * 0.5, width * 0.8]

    c.setFont("Helvetica", 9)
    for text, x in zip(sign_labels, positions):
        c.drawCentredString(x, footer_y, text)

    # Linee firma sotto
    signature_lines = ["_________________________", "_________________________", "_________________________"]
    for line, x in zip(signature_lines, positions):
        c.drawCentredString(x, footer_y - 20, line)

    c.save()

#with open("prova.json", "r", encoding="utf-8") as f:
#    data = json.load(f)
#generate_pdf_checkup(data, r"C:\Users\vince\Downloads\clinic_project (1)\clinic_project\report.pdf")
