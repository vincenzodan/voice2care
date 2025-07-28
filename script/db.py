from pymongo import MongoClient
import config
# Inserimento della stringa di connessione
connection_string = config.MONGODB_URI
client = MongoClient(connection_string)

# Creazione database e collezione 
db = client["clinic_db"]          
collection = db["clinical_data"] 

def update_document(doc_id, new_data):
    """
    Aggiorna il documento con _id = doc_id nel DB con i valori di new_data.
    doc_id: string o ObjectId
    new_data: dict con i campi da aggiornare
    """
    try:
        # Converti doc_id in ObjectId se è stringa

        if isinstance(doc_id, str):
            doc_id = ObjectId(doc_id)

        # Rimuovi eventuali campi vuoti o None (opzionale)
        update_fields = {k: v for k, v in new_data.items() if v not in (None, "")}

        result = collection.update_one(
            {"_id": doc_id},
            {"$set": update_fields}
        )
        if result.matched_count == 0:
            return False, "Documento non trovato"
        return True, "Documento aggiornato con successo"
    except Exception as e:
        return False, str(e)

def save_to_mongo(data):
    print("[DEBUG] Dati da inserire:")
    print(data)

    if "ID" not in data:
        print("[ERRORE] Campo 'ID' mancante. Impossibile aggiornare.")
        return

    query = {"ID": data["ID"]}
    update = {"$set": data}

    result = collection.update_one(query, update, upsert=True)

    if result.matched_count > 0:
        print(f"[DEBUG] Documento con ID {data['ID']} creato/aggiornato.")

def get_all_documents():
    docs = list(collection.find())
    return docs

def get_latest_document():
    doc = collection.find_one(sort=[("_id", -1)])
    return doc

