import json

# Carica i dati ATT&CK dal file JSON
def load_attack_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Funzione per ottenere un oggetto MITRE ATT&CK per ID esterno (es. T1518)
def get_object_by_external_id(attack_data, external_id):
    for obj in attack_data['objects']:
        if 'external_references' in obj:
            for reference in obj['external_references']:
                if reference.get('external_id') == external_id:
                    return obj
    print(f"Nessun oggetto trovato per l'ID: {external_id}")
    return None

# Percorso del file JSON scaricato
file_path = 'C:\\Users\\Administrator\\Dropbox\\Sorgenti\\PYTHON\\0_Code\\enterprise-attack.json'

# Carica i dati ATT&CK
attack_data = load_attack_data(file_path)

# Esempio di ricerca per ID
external_id = input("Inserisci l'ID dell'oggetto da cercare (es. T1518): ")
obj = get_object_by_external_id(attack_data, external_id)

if obj:
    print("\nOggetto trovato:")
    print(f"ID: {obj['id']}")
    print(f"Nome: {obj.get('name', 'Nome non disponibile')}")
    print(f"Descrizione: {obj.get('description', 'Descrizione non disponibile')}\n")

    # Mostra informazioni aggiuntive, se presenti
    if 'type' in obj:
        print(f"Tipo di oggetto: {obj['type']}")
    if 'kill_chain_phases' in obj:
        print("Fasi della kill chain:")
        for phase in obj['kill_chain_phases']:
            print(f" - {phase['phase_name']}")
else:
    print("Nessun oggetto trovato con l'ID fornito.")
