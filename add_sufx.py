"""
Rinomina i file aggiungendo un suffisso al nome
"""


import os

# Definisci la cartella in cui si trovano i file
cartella = "C:\\Users\\Administrator\\Downloads\\imm\\Nuovacartella"

# Definisci il suffisso da aggiungere
suffisso = "_a"

# Verifica che la cartella esista
if os.path.exists(cartella) and os.path.isdir(cartella):
    # Scandisce tutti i file nella cartella
    for filename in os.listdir(cartella):
        # Estrae il nome del file e l'estensione
        nome_file, estensione = os.path.splitext(filename)
        # Verifica che il nome del file non contenga già il suffisso
        if not nome_file.endswith(suffisso):
            # Crea il nuovo nome del file con il suffisso aggiunto prima dell'estensione
            nuovo_nome = nome_file + suffisso + estensione
            # Rinomina il file
            vecchio_percorso = os.path.join(cartella, filename)
            nuovo_percorso = os.path.join(cartella, nuovo_nome)
            os.rename(vecchio_percorso, nuovo_percorso)
            print(f"Rinominato: {filename} -> {nuovo_nome}")
else:
    print(f"La cartella '{cartella}' non esiste.")
