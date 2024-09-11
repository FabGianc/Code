"""
Utilizzo:
Scarica il file JSON dal link 

https://github.com/mitre-attack/attack-stix-data/tree/master/enterprise-attack

e specifica il percorso corretto nel codice.
Esegui lo script per cercare oggetti specifici e visualizzare i dettagli correlati.

"""


import json

# Carica i dati ATT&CK dal file JSON
def load_attack_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Funzione per ottenere un oggetto MITRE ATT&CK per ID
def get_object_by_id(attack_data, object_id):
    for obj in attack_data['objects']:
        if obj.get('id') == object_id:
            return obj
    print(f"Nessun oggetto trovato per l'ID: {object_id}")
    return None

# Funzione per ottenere oggetti correlati
def get_related_objects(obj, attack_data):
    related = []
    if obj:
        if 'object_marking_refs' in obj:
            for ref in obj['object_marking_refs']:
                for other_obj in attack_data['objects']:
                    if ref == other_obj.get('id'):
                        related.append(other_obj)
    return related

# Percorso del file JSON scaricato
file_path = "C:\\percorso_completp_cartella\\enterprise-attack.json"      # Windows

# Carica i dati ATT&CK
attack_data = load_attack_data(file_path)

# Esempio di ricerca per ID
object_id = input("Inserisci l'ID dell'oggetto da cercare: ")
obj = get_object_by_id(attack_data, object_id)

if obj:
    print("\nOggetto trovato:")
    print(f"ID: {obj['id']}")
    print(f"Nome: {obj.get('name', 'Nome non disponibile')}")
    print(f"Descrizione: {obj.get('description', 'Descrizione non disponibile')}\n")

    # Ottieni e mostra gli oggetti correlati
    related_objects = get_related_objects(obj, attack_data)
    if related_objects:
        print("Oggetti correlati trovati:")
        for related in related_objects:
            print(f"- ID: {related['id']}, Tipo: {related.get('type', 'Tipo non disponibile')}, Nome: {related.get('name', 'Nome non disponibile')}")
    else:
        print("Nessun oggetto correlato trovato.")
