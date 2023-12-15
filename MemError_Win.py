"""
Questo script alloca dinamicamente blocchi di memoria 
fino a quando si verifica un MemoryError. 
"""


# WARNING: Esegui questo script solo a scopo educativo e in un ambiente di test!

import ctypes
import psutil

def get_memory_usage():
    memory = psutil.virtual_memory()
    print(f"Memoria totale: {memory.total} bytes")
    print(f"Memoria disponibile: {memory.available} bytes")
    print(f"Memoria in uso: {memory.used} bytes")
    print(f"Percentuale di memoria utilizzata: {memory.percent}%")


def consume_memory(memory_size_mb):
    # Alloca dinamicamente la memoria in base al valore fornito in input
    memory_blocks = []
    try:
        while True:
            block = ctypes.create_string_buffer(memory_size_mb * 1024 * 1024)
            memory_blocks.append(block)
            get_memory_usage()
    except MemoryError:
        print(f"Memory esaurita con allocazione di {memory_size_mb} MB")

if __name__ == "__main__":
    try:
        print("Questo script alloca dinamicamente blocchi di memoria fino a quando si verifica un MemoryError.")
        memory_size = int(input("Inserisci la dimensione della memoria in MB: "))
        consume_memory(memory_size)
    except ValueError:
        print("Inserisci un valore valido.")
