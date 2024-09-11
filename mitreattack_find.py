"""
Script Python che esplora le cartelle nella directory "atomics" per una tecnica MITRE ATT&CK specifica
(ad esempio, T1001.002, T1055, T1218.003, ecc.) e mostra il contenuto del file .md associato.

Esegui lo script, inserisci l'ID della tecnica quando richiesto (ad esempio, T1001.002) 
e lo script esplorerà la cartella e mostrerà il contenuto di tutti i file .md presenti.

NOTE:
Atomic Red Team™ è una libreria di test mappati al framework MITRE ATT&CK®. 
I team di sicurezza possono utilizzare Atomic Red Team per testare i propri ambienti in modo rapido, 
portabile e riproducibile.

Scarica Atomic Red Team™ da https://github.com/redcanaryco/atomic-red-team
"""


import os

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

# Esempio di utilizzo
if __name__ == "__main__":
    # Sostituisci con il percorso della cartella "atomics"
    # base_path = "/home/kali/atomic-red-team/atomics/"     # Linux
    base_path = "C:\\AtomicRedTeam\\atomics"                # Windows
    tecnica_id = input("Inserisci l'ID della tecnica MITRE ATT&CK (es. T1001.002, T1055, T1218.003): ")
    esplora_cartella_tecnica(base_path, tecnica_id)