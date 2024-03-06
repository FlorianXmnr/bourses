import yfinance as yf
from datetime import datetime, timedelta
import os
from pymongo import MongoClient

# from connection import *

user = os.environ.get("MONGO_USER")
password = os.environ.get("MONGO_PASSWORD")
host = os.environ.get("MONGO_HOST")
dbname = os.environ.get("MONGO_DBNAME")
collection_name = os.environ.get("MONGO_COLLECTION_NAME")
app_name = os.environ.get("MONGO_APP_NAME")
uri = f"mongodb+srv://{user}:{password}@{host}/{dbname}?retryWrites=true&w=majority&appName={app_name}&tls=true"

print(uri)
client = MongoClient(uri)

client = MongoClient(uri)

# Sélectionner la base de données
db = client[dbname]

# Sélectionner la collection dans laquelle vous souhaitez insérer les données
collection = db[collection_name]

# Calculer la date de la veille
today = datetime.now()
if today.weekday() == 0:
    hier = today - timedelta(days=3)
else:
    hier = today - timedelta(days=1)

date_format_yfinance = hier.strftime('%Y-%m-%d')  # Format pour yfinance
date_format_db = hier.strftime('%d/%m/%Y')  # Format pour la base de données

symboles = ["MC.PA", "RMS.PA", "OR.PA", "CDI.PA", "TTE.PA", "AIR.PA", "SU.PA", "SAN.PA", "AI.PA", "EL.PA", "SAF.PA",
            "CS.PA", "DG.PA", "BNP.PA", "DSY.PA", "KER.PA",
            "BN.PA"]

for symbole in symboles:
    action = yf.Ticker(symbole)
    historique = action.history(start=date_format_yfinance, end=datetime.now().strftime('%Y-%m-%d'))
    if not historique.empty:
        dernier = historique.iloc[-1]
        document = {
            'Date': date_format_db,  # Utilisez le format de date pour la base de données
            'Open': dernier['Open'],
            'High': dernier['High'],
            'Low': dernier['Low'],
            'Close': dernier['Close'],
            'Volume': dernier['Volume'],
            'Symbole': symbole
        }
        collection.insert_one(document)
        print(f"Inséré : {document}")
    else:
        print(f"Aucune donnée trouvée pour {symbole} à la date {date_format_db}.")
