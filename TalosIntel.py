"""
Script di python per interrogare Talos Intelligence. 
Talos Intelligence è un servizio di threat intelligence di Cisco che fornisce informazioni 
su minacce e reputazione degli indirizzi IP.

"""


import requests

def query_talos(ip_address):
    url = f"https://talosintelligence.com/cloud_intelligence/api/v2/details/ip/{ip_address}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Errore nella richiesta: {response.status_code}"

# Esempio di utilizzo
ip_to_check = "8.8.8.8"
result = query_talos(ip_to_check)
print(result)