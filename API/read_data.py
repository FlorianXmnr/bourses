from connection import *
from datetime import datetime, timedelta

symboles = ["MC.PA", "RMS.PA", "OR.PA", "CDI.PA", "TTE.PA", "AIR.PA", "SU.PA", "SAN.PA", "AI.PA", "EL.PA", "SAF.PA",
            "CS.PA", "DG.PA", "BNP.PA", "DSY.PA", "KER.PA","BN.PA"]
# Sélectionner la base de données
db = client[dbname]

# Sélectionner la collection dans laquelle vous souhaitez insérer les données
collection = db[collection_name]
print(collection)
# Calculer la date de la veille
today = datetime.now()
if today.weekday() == 0:
    hier = today - timedelta(days=3)
else:
    hier = today - timedelta(days=1)
# Calculer la date d'hier
hier = hier.strftime('%d/%m/%Y')  # Formattez selon le format de date dans votre base de données

for symbole in symboles:
    # Trouver le document pour le symbole à la date d'hier
    document = collection.find_one({"Symbole": symbole, "Date": hier})
    if document:
        print(f"Dernière donnée pour {symbole} à la date d'hier : {document}")
    else:
        print(f"Aucune donnée trouvée pour {symbole} à la date d'hier.")
