import nasdaqdatalink

nasdaqdatalink.ApiConfig.api_key = "N5kmWx22fUu1scWxZbBU"


import requests

# Remplacez par votre clé API Quandl
API_KEY = "N5kmWx22fUu1scWxZbBU"

# Remplacez par le code dataset de LVMH sur Quandl
DATASET_CODE = "LVMHF"

url = f"https://www.quandl.com/api/v3/datasets/{DATASET_CODE}/data.json?api_key={API_KEY}"

response = requests.get(url)
data = response.json()

# Afficher les données historiques
print(data)
