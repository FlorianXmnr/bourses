import requests

API_KEY = "EV9WDCUC2WGFF55J"

recherche_symbole = 'TTE'

url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={recherche_symbole}&apikey={API_KEY}"

response = requests.get(url)
data = response.json()

print(data)
