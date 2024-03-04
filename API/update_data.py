import yfinance as yf
from datetime import datetime, timedelta
# from connection import dbname,collection_name, symboles

from pymongo import MongoClient

user = "alexiszueraspro"
password = "DJK7hi0GRSkl8upZ"
host = "clusterbourse.60a6vhb.mongodb.net"
dbname = "Stage"
collection_name = "Bourse"
symboles = ["MC.PA", "RMS.PA", "OR.PA", "CDI.PA", "TTE.PA", "AIR.PA", "SU.PA", "SAN.PA", "AI.PA", "EL.PA", "SAF.PA",
            "CS.PA", "DG.PA", "BNP.PA", "DSY.PA", "KER.PA",
            "BN.PA"]
# URI de connexion
uri = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority&appName=ClusterBourse"
# Se connecter à MongoDB
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
