"""
Script python che attraverso più API chiede ai seguenti servizi, informazioni sulla reputazione 
di domini o IP:

VirusTotal: Mostra informazioni WHOIS sul dominio, gli IP risolti, 
            le URL rilevate come sospette e i domini correlati
IBM X-Force Exchange (Previa sottoscrozione abbonamento premium)
URLScan.io: Visualizza l'URL scansionato, l'IP, il server, il titolo del sito 
            e la validità del certificato TLS, oltre al link per uno screenshot.
AAbuseIPDB: Visualizza informazioni dettagliate sull'indirizzo IP, inclusi il punteggio di abuso, 
            il tipo di utilizzo (es. hosting web), il provider di servizi Internet (ISP) 
            e se l'IP è stato segnalato nella rete Tor.

E' possibile aggiungere ulteriori servizi in modo simile, assicurandoti che ogni API segua 
le specifiche e il formato di chiamata corretto.

L'output è formattato

"""

import requests
from colorama import init, Fore, Style

# Inizializzazione di colorama
init(autoreset=True)

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

# Funzione per formattare l'output di VirusTotal
def format_virustotal_output(result):
    output = Fore.CYAN + f"\nVirusTotal Results for domain:\n" + Style.RESET_ALL
    if result['response_code'] == 1:
        output += Fore.GREEN + f" - Domain WHOIS Info:\n{result.get('whois', 'N/A')}\n"
        output += Fore.GREEN + f" - Resolved IPs:\n"
        for resolution in result.get('resolutions', []):
            output += f"   - {resolution['ip_address']} (Last resolved: {resolution['last_resolved']})\n"
        output += Fore.GREEN + f" - Detected URLs:\n"
        for detected_url in result.get('detected_urls', []):
            output += f"   - {detected_url['url']} (Positives: {detected_url['positives']}/{detected_url['total']})\n"
        output += Fore.GREEN + f" - Domain Siblings:\n{', '.join(result.get('domain_siblings', [])) or 'None'}\n"
    else:
        output += Fore.RED + " - No data found for this domain.\n"
    return output

# Funzione per formattare l'output di URLScan.io
def format_urlscan_output(result):
    output = Fore.CYAN + f"\nURLScan.io Results:\n" + Style.RESET_ALL
    for entry in result.get('results', []):
        task = entry['task']
        page = entry['page']
        output += Fore.GREEN + f" - Scanned URL: {task['url']}\n"
        output += f"   - Domain: {task['domain']}\n"
        output += f"   - IP: {page['ip']} (Country: {page['country']})\n"
        output += f"   - Server: {page['server']}\n"
        output += f"   - Title: {page['title']}\n"
        output += f"   - TLS Validity: {page['tlsValidDays']} days (From: {page['tlsValidFrom']})\n"
        output += f"   - Screenshot: {entry['screenshot']}\n"
    return output

# Funzione per formattare l'output di AbuseIPDB
def format_abuseipdb_output(result):
    output = Fore.CYAN + f"\nAbuseIPDB Results for IP:\n" + Style.RESET_ALL
    if 'data' in result:
        data = result['data']
        output += Fore.GREEN + f" - IP Address: {data.get('ipAddress', 'N/A')}\n"
        output += f" - Is Public: {data.get('isPublic', 'N/A')}\n"
        output += f" - IP Version: {data.get('ipVersion', 'N/A')}\n"
        output += f" - Is Whitelisted: {data.get('isWhitelisted', 'N/A')}\n"
        output += f" - Abuse Confidence Score: {data.get('abuseConfidenceScore', 'N/A')}\n"
        output += f" - Country Code: {data.get('countryCode', 'N/A')}\n"
        output += f" - Usage Type: {data.get('usageType', 'N/A')}\n"
        output += f" - ISP: {data.get('isp', 'N/A')}\n"
        output += f" - Domain: {data.get('domain', 'N/A')}\n"
        output += f" - Hostnames: {', '.join(data.get('hostnames', []))}\n"
        output += f" - Is Tor: {data.get('isTor', 'N/A')}\n"
        output += f" - Total Reports: {data.get('totalReports', 'N/A')}\n"
        output += f" - Number of Distinct Users: {data.get('numDistinctUsers', 'N/A')}\n"
        output += f" - Last Reported At: {data.get('lastReportedAt', 'N/A')}\n"
    else:
        output += Fore.RED + " - No data found for this IP.\n"
    return output

# Funzione principale per gestire l'input dell'utente
def main():
    # Inserisci qui le tue chiavi API per i vari servizi
    api_keys = {
        'virustotal': 'your_virustotal_api_key',
        'ibm_xforce': 'your_ibm_xforce_api_key',
        'urlscan': 'your_urlscan_api_ke',
        'abuseipdb': 'your_abuseipdb_api_key',
    }

    # Richiesta di input per il tipo di analisi
    choice = input(Fore.YELLOW + "Vuoi analizzare un dominio o un IP? Inserisci 'dominio' o 'IP': " + Style.RESET_ALL).strip().lower()

    if choice == 'dominio':
        domain = input(Fore.YELLOW + "Inserisci il dominio da analizzare: " + Style.RESET_ALL).strip()
        # Interrogazione VirusTotal
        results = {}
        if api_keys.get('virustotal'):
            print(Fore.YELLOW + f"Querying VirusTotal for {domain}...")
            results['virustotal'] = query_virustotal(domain, api_keys['virustotal'])
        # Interrogazione URLScan.io
        if api_keys.get('urlscan'):
            print(Fore.YELLOW + f"Querying URLScan.io for {domain}...")
            results['urlscan'] = query_urlscan(domain, api_keys['urlscan'])

        # Formattare e visualizzare i risultati
        if 'virustotal' in results:
            print(format_virustotal_output(results['virustotal']))
        if 'urlscan' in results:
            print(format_urlscan_output(results['urlscan']))

    elif choice == 'ip':
        # Richiesta di input per l'analisi IP
        ip = input(Fore.YELLOW + "Inserisci l'IP da analizzare: " + Style.RESET_ALL).strip()
        print(Fore.YELLOW + f"Querying AbuseIPDB for {ip}...")

        # Effettua la query a AbuseIPDB
        results = query_abuseipdb(ip, api_keys['abuseipdb'])

         # Verifica se i risultati sono stati restituiti correttamente
        if results:
            print(Fore.YELLOW + "Risposta da AbuseIPDB ricevuta con successo!")
            print(format_abuseipdb_output(results))
        else:
            print(Fore.RED + "Nessun risultato ricevuto da AbuseIPDB.")

    else:
        print(Fore.RED + "Scelta non valida! Esegui nuovamente il programma e scegli 'dominio' o 'IP'." + Style.RESET_ALL)

# Esegui lo script
if __name__ == '__main__':
    main()
