"""
Questo script alloca dinamicamente blocchi di memoria 
fino a quando si verifica un MemoryError. 
"""


# WARNING: Esegui questo script solo a scopo educativo e in un ambiente di test!

import ctypes

def consume_memory():
    # Alloca dinamicamente la memoria in modo da esaurirla
    memory_blocks = []
    try:
        while True:
            block = ctypes.create_string_buffer(1024 * 1024)  # 1 MB
            memory_blocks.append(block)
    except MemoryError:
        print("Memory esaurita")

if __name__ == "__main__":
    consume_memory()
