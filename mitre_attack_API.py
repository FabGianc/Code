"""
Script Python che utilizza la libreria attackcti per interrogare 
il set di dati MITRE ATT&CK per oggetti correlati

pip install attackcti

NOTE:
Atomic Red Team™ è una libreria di test mappati al framework MITRE ATT&CK®. 
I team di sicurezza possono utilizzare Atomic Red Team per testare i propri ambienti in modo rapido, 
portabile e riproducibile.

Eventuali messaggi di warning sono generati dalla libreria TAXII2 client che attackcti utilizza 
per comunicare con il server MITRE ATT&CK. Questi avvisi non influenzano il funzionamento del programma, 
ma indicano che il client sta adattando le sue richieste in base alle risposte del server.
"""


import attackcti

def main():
    # Inizializza l'API ATT&CK
    attack = attackcti.attack_client()

    while True:
        print("\nMenù:")
        print("1. Cerca una tecnica per ID")
        print("2. Cerca tecniche per nome")
        print("3. Mostra tattiche correlate a una tecnica")
        print("4. Esci")
        
        scelta = input("Inserisci il numero dell'opzione desiderata: ")
        
        if scelta == "1":
            cerca_per_id(attack)
        elif scelta == "2":
            cerca_per_nome(attack)
        elif scelta == "3":
            mostra_correlati(attack)
        elif scelta == "4":
            print("Arrivederci!")
            break
        else:
            print("Opzione non valida. Riprova.")

def cerca_per_id(attack):
    tecnica_id = input("Inserisci l'ID della tecnica (es. T1595): ")
    tecniche = attack.get_techniques()
    tecnica = next((t for t in tecniche if t['external_references'][0]['external_id'] == tecnica_id), None)
    if tecnica:
        print(f"Tecnica trovata: {tecnica['name']} ({tecnica['external_references'][0]['external_id']})")
    else:
        print("Tecnica non trovata.")

def cerca_per_nome(attack):
    nome = input("Inserisci il nome o parte del nome della tecnica: ")
    tecniche = attack.get_techniques()
    risultati = [t for t in tecniche if nome.lower() in t['name'].lower()]
    if risultati:
        print("Tecniche trovate:")
        for tecnica in risultati:
            print(f"- {tecnica['name']} ({tecnica['external_references'][0]['external_id']})")
    else:
        print("Nessuna tecnica trovata.")

def mostra_correlati(attack):
    tecnica_id = input("Inserisci l'ID della tecnica per cui vuoi trovare le tattiche correlate: ")
    tecniche = attack.get_techniques()
    tecnica = next((t for t in tecniche if t['external_references'][0]['external_id'] == tecnica_id), None)
    if tecnica:
        print(f"Tattiche correlate a {tecnica['name']} ({tecnica['external_references'][0]['external_id']}):")
        tattiche = attack.get_tactics()
        for fase in tecnica.get('kill_chain_phases', []):
            tattica = next((t for t in tattiche if t['x_mitre_shortname'] == fase['phase_name']), None)
            if tattica:
                print(f"- {tattica['name']} ({tattica['external_references'][0]['external_id']})")
    else:
        print("Tecnica non trovata.")

if __name__ == "__main__":
    main()