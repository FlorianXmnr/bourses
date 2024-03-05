from connection import *
from datetime import datetime, timedelta
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
    document = collection_name.find_one({"Symbole": symbole, "Date": hier})
    if document:
        print(f"Dernière donnée pour {symbole} à la date d'hier : {document}")
    else:
        print(f"Aucune donnée trouvée pour {symbole} à la date d'hier.")
