import yfinance as yf
from connection import *
import pandas as pd

# Liste des symboles des 10 plus grandes entreprises françaises
symboles = ["MC.PA", "RMS.PA", "OR.PA", "CDI.PA", "TTE.PA", "AIR.PA", "SU.PA", "SAN.PA", "AI.PA", "EL.PA", "SAF.PA",
            "CS.PA", "DG.PA", "BNP.PA", "DSY.PA", "KER.PA", "BN.PA"]  # Complétez cette liste avec les symboles réels
# Sélectionner la base de données
db = client[dbname]

# Sélectionner la collection dans laquelle vous souhaitez insérer les données
collection = db[collection_name]
print(collection)
# Connexion à MongoDB


"""for symbole in symboles:
    action = yf.Ticker(symbole)
    try:
        historique = action.history(period="max")
        if 'Dividends' in historique.columns and 'Stock Splits' in historique.columns:
            historique = historique.drop(columns=['Dividends', 'Stock Splits'])
        historique = historique.reset_index()
        historique['Date'] = historique['Date'].dt.strftime('%d/%m/%Y')
        historique["Symbole"] = symbole
        # Convertir le DataFrame en liste de dictionnaires
        records = historique.to_dict('records')

        # Insérer les données dans MongoDB
        collection.insert_many(records)
        # Ici, vous pouvez ajouter le code pour insérer les données dans MongoDB
    except Exception as e:
        print(f"Erreur avec le symbole {symbole}: {e}")"""

for symbole in symboles:
    action = yf.Ticker(symbole)
    try:
        historique = action.history(period="max")
        if not historique.empty:
            if 'Dividends' in historique.columns and 'Stock Splits' in historique.columns:
                historique = historique.drop(columns=['Dividends', 'Stock Splits'])
            historique = historique.reset_index()
            if pd.api.types.is_datetime64_any_dtype(historique['Date']):
                historique['Date'] = historique['Date'].dt.strftime('%d/%m/%Y')
                # Ici, insérez les données dans MongoDB ou autre traitement
            historique["Symbole"] = symbole
        # Convertir le DataFrame en liste de dictionnaires
        records = historique.to_dict('records')

        # Insérer les données dans MongoDB
        collection.insert_many(records)
    except Exception as e:
        print(f"Erreur avec le symbole {symbole}: {e}")


"""# Requête pour voir les symboles
symboles_find = collection.find({}, {"Symbol": 1, "_id": 0})
for symbole in symboles_find:
    print(symbole)"""
