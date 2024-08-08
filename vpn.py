"""
Per verificare se un indirizzo IP proviene da una VPN, puoi usare un servizio di rilevamento IP 
o un database che classifichi gli indirizzi IP in base al loro uso (ad esempio, se appartengono 
a fornitori di servizi VPN, proxy, o sono IP aziendali). 
Una soluzione comune è utilizzare un'API esterna che fornisca queste informazioni. 

Script Python che utilizza l'API gratuita ipinfo.io per ottenere informazioni dettagliate 
su un indirizzo IP, compreso se è noto per essere utilizzato da una VPN.

Occorre ottenere un token API gratuito da ipinfo.io registrandoti sul loro sito. 

"""


import requests

def check_if_vpn(ip_address, access_token):
    url = f"https://ipinfo.io/{ip_address}/json?token={access_token}"
    response = requests.get(url)
    ip_data = response.json()
    
    # Verifica la presenza della chiave 'privacy' che contiene informazioni sulle VPN
    if 'privacy' in ip_data:
        vpn_status = ip_data['privacy'].get('vpn', False)
        return vpn_status
    else:
        return "No privacy data available"

# Sostituisci 'YOUR_ACCESS_TOKEN' con il tuo token API personale

ip_address = input("Inserisci l'indirizzi IP da verificare: ")
# ip_address = "87.101.94.67"  # Sostituisci questo con l'indirizzo IP da verificare
access_token = '6c76be6b154104' # 'YOUR_ACCESS_TOKEN'
vpn_status = check_if_vpn(ip_address, access_token)

print("Is the IP address a VPN?:", vpn_status)
