"""
Questo script utilizza il modulo psutil per ottenere informazioni sulla memoria virtuale 
del sistema e quindi stampa alcune informazioni, come la memoria totale, 
la memoria disponibile, la memoria in uso e la percentuale di memoria utilizzata.

Assicurati di aver installato il modulo psutil prima di eseguire lo script. 
Puoi farlo usando il seguente comando
pip3 install psutil

"""

import psutil

def get_memory_usage():
    memory = psutil.virtual_memory()
    print(f"Memoria totale: {memory.total} bytes")
    print(f"Memoria disponibile: {memory.available} bytes")
    print(f"Memoria in uso: {memory.used} bytes")
    print(f"Percentuale di memoria utilizzata: {memory.percent}%")

if __name__ == "__main__":
    get_memory_usage()
