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
        return

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

# Esempio di utilizzo
if __name__ == "__main__":
    technique_id = input("Inserisci l'ID della tecnica MITRE ATT&CK (es. T1001.002, T1055, T1218.003): ")
    fetch_mitre_technique(technique_id)
