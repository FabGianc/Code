"""
Script python che attraverso più API chiede ai seguenti servizi, informazioni sulla reputazione 
di domini o IP:

VirusTotal
IBM X-Force Exchange
URLScan.io
AbuseIPDB

E' possibile aggiungere ulteriori servizi in modo simile, assicurandoti che ogni API segua 
le specifiche e il formato di chiamata corretto.
"""

import requests

# Funzione per interrogare VirusTotal
def query_virustotal(domain, api_key):
    url = 'https://www.virustotal.com/vtapi/v2/domain/report'
    params = {'apikey': api_key, 'domain': domain}
    response = requests.get(url, params=params)
    return response.json()

# Funzione per interrogare IBM X-Force Exchange
def query_ibm_xforce(domain, api_key):
    url = f'https://api.xforce.ibmcloud.com/api/url/{domain}'
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    return response.json()

# Funzione per interrogare URLScan.io
def query_urlscan(domain, api_key):
    url = 'https://urlscan.io/api/v1/search/'
    headers = {'API-Key': api_key}
    params = {'q': domain}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Funzione per interrogare AbuseIPDB (per gli IP)
def query_abuseipdb(ip, api_key):
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {'Key': api_key, 'Accept': 'application/json'}
    params = {'ipAddress': ip, 'maxAgeInDays': '90'}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Funzione principale che interroga tutti i servizi per il dominio
def query_all_services_domain(domain, api_keys):
    results = {}

    # Interrogazione VirusTotal
    if api_keys.get('virustotal'):
        print(f"Querying VirusTotal for {domain}...")
        vt_result = query_virustotal(domain, api_keys['virustotal'])
        results['virustotal'] = vt_result

    # Interrogazione IBM X-Force
    if api_keys.get('ibm_xforce'):
        print(f"Querying IBM X-Force for {domain}...")
        xforce_result = query_ibm_xforce(domain, api_keys['ibm_xforce'])
        results['ibm_xforce'] = xforce_result

    # Interrogazione URLScan.io
    if api_keys.get('urlscan'):
        print(f"Querying URLScan.io for {domain}...")
        urlscan_result = query_urlscan(domain, api_keys['urlscan'])
        results['urlscan'] = urlscan_result

    return results

# Funzione principale che interroga tutti i servizi per l'IP
def query_all_services_ip(ip, api_keys):
    results = {}

    # Interrogazione AbuseIPDB
    if api_keys.get('abuseipdb'):
        print(f"Querying AbuseIPDB for {ip}...")
        abuseipdb_result = query_abuseipdb(ip, api_keys['abuseipdb'])
        results['abuseipdb'] = abuseipdb_result

    return results

# Funzione principale per gestire l'input dell'utente
def main():
    # Inserisci qui le tue chiavi API per i vari servizi
    api_keys = {
        'virustotal': '8f644a775d7154a1f46d98ce98d85be652629ad29fa1693e9baecda5692724d9',
        # IBM è a pagamento, per ora commento la riga
        # 'ibm_xforce': 'your_ibm_xforce_api_key',
        'urlscan': '2741814b-c42b-4f4a-b2db-391b257db18c',
        'abuseipdb': 'f010dce7a9825a178727768ef81213adc5b595aed54cab5814ed75adcbabb01fdaaa41394b616c56',
    }

    # Richiesta di input per il tipo di analisi
    choice = input("Vuoi analizzare un dominio o un IP? Inserisci 'dominio' o 'IP': ").strip().lower()

    if choice == 'dominio':
        domain = input("Inserisci il dominio da analizzare: ").strip()
        results = query_all_services_domain(domain, api_keys)
    elif choice == 'ip':
        ip = input("Inserisci l'IP da analizzare: ").strip()
        results = query_all_services_ip(ip, api_keys)
    else:
        print("Scelta non valida! Esegui nuovamente il programma e scegli 'dominio' o 'IP'.")
        return

    # Visualizzazione risultati
    for service, result in results.items():
        print(f"\nResults from {service}:")
        print(result)

# Esegui lo script
if __name__ == '__main__':
    main()

