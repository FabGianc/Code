"""
Il protocollo STUN, acronimo di Session Traversal Utilities for NAT, 
è un protocollo di rete utilizzato per scopi di traversamento di reti (NAT) 
in ambienti di comunicazione in tempo reale, come le chiamate vocali e video su Internet. 
Il suo scopo principale è consentire a dispositivi di comunicare attraverso un 
Network Address Translator (NAT) o un firewall, che altrimenti potrebbe impedire 
o complicare la comunicazione diretta tra di loro.

STUN è spesso utilizzato in situazioni in cui i dispositivi si trovano dietro un NAT, 
che è comunemente utilizzato per condividere un singolo indirizzo IP pubblico 
tra più dispositivi in una rete locale. Il NAT può causare problemi nelle comunicazioni 
peer-to-peer, poiché i dispositivi esterni non possono raggiungere direttamente quelli interni.

Quando un dispositivo si trova dietro un NAT, utilizza STUN per scoprire il proprio 
indirizzo IP pubblico e la porta attraverso la quale il NAT instrada il traffico in arrivo. 
Queste informazioni possono quindi essere comunicate ad altri dispositivi 
con cui si vuole stabilire una comunicazione, consentendo loro di inviare dati a quel dispositivo 
attraverso il NAT.

STUN utilizza di solito la porta UDP 3478. Esistono anche delle estensioni 
come TURN (Traversal Using Relay NAT) e ICE (Interactive Connectivity Establishment) 
che ampliano le funzionalità di STUN per affrontare scenari più complessi, 
come quando il NAT è di tipo "symmetric" o quando è presente un firewall.

La funzione stun.get_socket viene utilizzata per ottenere un socket STUN. 
Questo socket verrà poi utilizzato per effettuare una richiesta STUN al server specificato. 

NOTA:
- stun_host: Specifica l'host del server STUN a cui fare la richiesta. 
In questo caso, è impostato su "stun.l.google.com", che è un server STUN pubblico 
gestito da Google. 
I server STUN sono essenzialmente server intermedi che aiutano a scoprire 
l'indirizzo IP pubblico e la porta utilizzati da un dispositivo dietro un NAT.

- stun_port: Specifica la porta sulla quale effettuare la richiesta STUN. 
Di solito, la porta predefinita per STUN è 3478. Tuttavia, alcune implementazioni 
possono utilizzare altre porte.

pip install pystun3
"""

import stun

import socket

from ipwhois import IPWhois

''' 
La funzione domain_lookup() utilizza la libreria ipwhois per ottenere informazioni 
sul dominio associato a un indirizzo IP utilizzando il metodo lookup_rdap(). 
Se viene trovata una descrizione ASN nell'output, viene restituita la descrizione corrispondente. 
In caso contrario, viene restituito "N/D"
'''

def domain_lookup(ip_address):
    try:
        obj = IPWhois(ip_address)
        result = obj.lookup_rdap()
        if 'asn_description' in result:
            return result['asn_description']

        # Risoluzione DNS inversa per ottenere il nome host
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except Exception:
        pass
    return "N/D"

def discover_public_ip_and_port():
    # Ottieni le informazioni STUN dal server di Google
    nat_type, external_ip, external_port = stun.get_ip_info(stun_host="stun.l.google.com", stun_port=19302)

    # Stampa le informazioni ottenute
    print(f"Tipo di NAT: {nat_type}")
    print(f"Indirizzo IP pubblico: {external_ip}")
    print(f"Porta pubblica: {external_port}")
    print(f"IP lookup: {domain_lookup(external_ip)}")
if __name__ == "__main__":
    discover_public_ip_and_port()
