"""
Script Python che accetta come input un hash e un percorso in un volume. 
Lo script calcola gli hash di tutti i file nel percorso specificato 
e confronta ciascuno di essi con l'hash fornito. Se trova una corrispondenza, 
restituisce il nome del file e il percorso completo.
"""


import os
import hashlib

def calculate_hash(file_path, hash_type="sha256"):
    """
    Calcola l'hash di un file dato il suo percorso.
    :param file_path: Percorso del file
    :param hash_type: Tipo di hash
    :return: L'hash del file come stringa esadecimale
    """
    hash_func = hashlib.new(hash_type)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def select_hash_type():
    """
    Consente all'utente di selezionare il tipo di hash.
    :return: Tipo di hash come stringa
    """
    print("Seleziona il tipo di hash:")
    print("1 - MD5")
    print("2 - SHA1")
    print("3 - SHA256")
    print("4 - SHA512")
    
    choice = input("Inserisci il numero del tipo di hash desiderato: ")

    hash_types = {
        "1": "md5",
        "2": "sha1",
        "3": "sha256",
        "4": "sha512"
    }

    return hash_types.get(choice, "sha256")

def find_matching_file(target_hash, directory_path, hash_type="sha256"):
    """
    Cerca un file in una directory che abbia un hash corrispondente a quello fornito.
    :param target_hash: L'hash da confrontare
    :param directory_path: Il percorso della directory da analizzare
    :param hash_type: Tipo di hash
    :return: Nome del file e percorso se trovato, altrimenti None
    """
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_hash = calculate_hash(file_path, hash_type)
                if file_hash == target_hash:
                    return file, file_path
            except Exception as e:
                print(f"Errore nel calcolare l'hash per {file_path}: {e}")
    return None

# Esempio di utilizzo
if __name__ == "__main__":
    target_hash = input("Inserisci l'hash da confrontare: ")
    directory_path = input("Inserisci il percorso della directory: ")
    hash_type = select_hash_type()

    result = find_matching_file(target_hash, directory_path, hash_type)
    if result:
        file_name, file_path = result
        print(f"Trovato il file corrispondente: {file_name} nel percorso: {file_path}")
    else:
        print("Nessun file corrisponde all'hash fornito.")
