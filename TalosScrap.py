"""
Talos Intelligence non offre un'API pubblica ufficiale per l'accesso diretto alle sue informazioni, 
quindi questo script tenta l'uso di tecniche di web scraping.

"""


import requests
from bs4 import BeautifulSoup

def query_talos(domain):
    url = f'https://talosintelligence.com/reputation_center/lookup?search={domain}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Cerca i dettagli di reputazione nel contenuto della pagina
    result = soup.find('div', class_='network-record-info')
    if result:
        return result.text.strip()
    else:
        return "No data found or page structure changed."

# Esempio di utilizzo
domain = 'example.com'
reputation = query_talos(domain)
print(reputation)