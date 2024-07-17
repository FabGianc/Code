"""
    Muove il mouse di un numero specificato di pixel a intervalli regolari.
    
    :param interval: Intervallo di tempo (in secondi) tra i movimenti del mouse.
    :param pixels: Numero di pixel di cui muovere il mouse.

    necessita di pyautogui
    pip install pyautogui
"""

import pyautogui
import time

def move_mouse(interval=1, pixels=100):
    
    try:
        while True:
            current_position = pyautogui.position()
            # Muove il mouse di 'pixels' pixel a destra
            pyautogui.moveRel(pixels, 0, duration=0.25)
            time.sleep(0.5)  # Pausa per simulare il movimento
            pyautogui.moveTo(current_position, duration=1)  # Torna alla posizione originale
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Movimento del mouse interrotto.")

if __name__ == "__main__":
    move_mouse(interval=1, pixels=100)
