from connection import *
from datetime import datetime, timedelta
# Sélectionner la base de données
db = client[dbname]

# Sélectionner la collection dans laquelle vous souhaitez insérer les données
collection = db[collection_name]
print(collection)

hier = datetime.now() - timedelta(days=1)
hier_str = hier.strftime('%d/%m/%Y')  # Formattez selon le format de date dans votre base de données

for symbole in symboles:
    # Supprimer les documents pour le symbole à la date d'hier
    result = collection.delete_many({"Symbole": symbole, "Date": hier_str})
    print(f"Documents supprimés pour {symbole} à la date d'hier: {result.deleted_count}")

