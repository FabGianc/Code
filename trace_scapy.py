from scapy.all import *

MAX_HOPS = 30
TIMEOUT = 2

def get_route(destination):
    ans, _ = traceroute(destination, maxttl=MAX_HOPS, timeout=TIMEOUT)
    ans.graph()

try:
    # Richiedi all'utente di inserire l'hostname da tracciare
    hostname = input("Inserisci l'hostname da tracciare: ")
    get_route(hostname)
except KeyboardInterrupt:
    print("\nInterruzione manuale dell'esecuzione.")
