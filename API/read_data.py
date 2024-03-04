from connection import *
from datetime import datetime, timedelta

symboles = ["MC.PA", "RMS.PA", "OR.PA", "CDI.PA", "TTE.PA", "AIR.PA", "SU.PA", "SAN.PA", "AI.PA", "EL.PA", "SAF.PA",
            "CS.PA", "DG.PA", "BNP.PA", "DSY.PA", "KER.PA","BN.PA"]
# Sélectionner la base de données
db = client[dbname]

# Sélectionner la collection dans laquelle vous souhaitez insérer les données
collection = db[collection_name]
print(collection)

# Calculer la date d'hier
hier = datetime.now() - timedelta(days=1)
hier_str = hier.strftime('%d/%m/%Y')  # Formattez selon le format de date dans votre base de données

for symbole in symboles:
    # Trouver le document pour le symbole à la date d'hier
    document = collection.find_one({"Symbole": symbole, "Date": hier_str})
    if document:
        print(f"Dernière donnée pour {symbole} à la date d'hier : {document}")
    else:
        print(f"Aucune donnée trouvée pour {symbole} à la date d'hier.")
