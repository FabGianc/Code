"""
Script Python che:
1)  utilizza la libreria attackcti per interrogare il set di dati MITRE ATT&CK per oggetti correlati

2)  esplora le cartelle nella directory "atomics" per una tecnica MITRE ATT&CK specifica
    (ad esempio, T1001.002, T1055, T1218.003, ecc.) e mostra il contenuto del file .md associato.

pip install attackcti

NOTE:
Atomic Red Team™ è una libreria di test mappati al framework MITRE ATT&CK®. 
I team di sicurezza possono utilizzare Atomic Red Team per testare i propri ambienti in modo rapido, 
portabile e riproducibile.

Eventuali messaggi di warning sono generati dalla libreria TAXII2 client che attackcti utilizza 
per comunicare con il server MITRE ATT&CK. Questi avvisi non influenzano il funzionamento del programma, 
ma indicano che il client sta adattando le sue richieste in base alle risposte del server.

"""

import os
import attackcti

def fetch_mitre_technique(technique_id):
    lift = attackcti.attack_client()

    # Cerca la tecnica per ID
    techniques = lift.get_techniques()
    technique_info = None

    for technique in techniques:
        if technique['external_references'][0]['external_id'] == technique_id:
            technique_info = technique
            break

    if not technique_info:
        print(f"Nessuna informazione trovata per l'ID: {technique_id}")
        return None

    # Mostra le informazioni della tecnica
    print(f"ID: {technique_info['external_references'][0]['external_id']}")
    print(f"Nome: {technique_info['name']}")
    print(f"Descrizione: {technique_info['description']}\n")

    if 'x_mitre_platforms' in technique_info:
        print(f"Piattaforme: {', '.join(technique_info['x_mitre_platforms'])}")
    if 'kill_chain_phases' in technique_info:
        print("Fasi della kill chain:")
        for phase in technique_info['kill_chain_phases']:
            print(f" - {phase['phase_name']}")

    return technique_info

def esplora_cartella_tecnica(base_path, tecnica_id):
    # Costruisce il percorso completo della cartella
    tecnica_path = os.path.join(base_path, tecnica_id)

    # Verifica se la cartella esiste
    if not os.path.exists(tecnica_path):
        print(f"La cartella per la tecnica {tecnica_id} non esiste.")
        return

    # Cerca i file .md all'interno della cartella
    md_files = [f for f in os.listdir(tecnica_path) if f.endswith('.md')]

    if not md_files:
        print(f"Nessun file .md trovato nella cartella {tecnica_id}.")
        return

    # Mostra il contenuto di tutti i file .md trovati
    for md_file in md_files:
        md_file_path = os.path.join(tecnica_path, md_file)
        print(f"\nContenuto del file {md_file_path}:\n")
        with open(md_file_path, 'r', encoding='utf-8') as file:
            print(file.read())
            print("-" * 40)  # Separatore tra contenuti di diversi file

def main():
    # Sostituisci con il percorso della cartella "atomics"
    # base_path = "/home/kali/atomic-red-team/atomics/"     # Linux
    base_path = "C:\\AtomicRedTeam\\atomics"                # Windows
        
    while True:
        print("\nMenù:")
        print("1. Cerca una tecnica per ID")
        print("2. Cerca tecniche per nome")
        print("3. Mostra tattiche correlate a una tecnica")
        print("4. Esplora cartella tecnica per file .md")
        print("5. Esci")
        
        scelta = input("Inserisci il numero dell'opzione desiderata: ")
        
        if scelta == "1":
            technique_id = input("Inserisci l'ID della tecnica MITRE ATT&CK (es. T1001.002, T1055, T1218.003): ")
            fetch_mitre_technique(technique_id)
        elif scelta == "2":
            cerca_per_nome()
        elif scelta == "3":
            mostra_correlati()
        elif scelta == "4":
            technique_id = input("Inserisci l'ID della tecnica MITRE ATT&CK (es. T1001.002, T1055, T1218.003): ")
            esplora_cartella_tecnica(base_path, technique_id)
        elif scelta == "5":
            print("Arrivederci!")
            break
        else:
            print("Opzione non valida. Riprova.")

def cerca_per_nome():
    lift = attackcti.attack_client()
    nome = input("Inserisci il nome o parte del nome della tecnica: ")
    tecniche = lift.get_techniques()
    risultati = [t for t in tecniche if nome.lower() in t['name'].lower()]
    if risultati:
        print("Tecniche trovate:")
        for tecnica in risultati:
            print(f"- {tecnica['name']} ({tecnica['external_references'][0]['external_id']})")
    else:
        print("Nessuna tecnica trovata.")

def mostra_correlati():
    lift = attackcti.attack_client()
    tecnica_id = input("Inserisci l'ID della tecnica per cui vuoi trovare le tattiche correlate: ")
    tecniche = lift.get_techniques()
    tecnica = next((t for t in tecniche if t['external_references'][0]['external_id'] == tecnica_id), None)
    if tecnica:
        print(f"Tattiche correlate a {tecnica['name']} ({tecnica['external_references'][0]['external_id']}):")
        tattiche = lift.get_tactics()
        for fase in tecnica.get('kill_chain_phases', []):
            tattica = next((t for t in tattiche if t['x_mitre_shortname'] == fase['phase_name']), None)
            if tattica:
                print(f"- {tattica['name']} ({tattica['external_references'][0]['external_id']})")
    else:
        print("Tecnica non trovata.")

if __name__ == "__main__":
    main()
