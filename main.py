import yfinance as yf
from connection import *

# Remplacer 'BN.PA' par le symbole de votre choix
symbole = 'BN.PA'  # Exemple pour BNP Paribas, cotée sur Euronext Paris
action = yf.Ticker(symbole)

# Récupérer les données historiques
historique = action.history(period="max")  # 'max' pour l'historique complet, ou '1mo', '1y', etc.

historique = historique.drop(columns=['Dividends', 'Stock Splits'])

# Réinitialiser l'index pour transformer les dates d'index en une colonne "Date"
historique = historique.reset_index()
historique['Date'] = historique['Date'].dt.strftime('%d/%m/%Y')

# Afficher les premières lignes pour vérifier
print(historique.head())

# Sélectionner la base de données
db = client[dbname]

# Sélectionner la collection dans laquelle vous souhaitez insérer les données
collection = db[collection_name]
print(collection)

# Convertir le DataFrame 'historique' en liste de dictionnaires
records = historique.to_dict('records')

# Insérer les données dans la collection MongoDB
try:
    collection.insert_many(records)
    print("Les données ont été insérées avec succès dans MongoDB.")
except Exception as e:
    print("Une erreur s'est produite lors de l'insertion des données :", e)
