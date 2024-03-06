from connection import *
import csv
from datetime import datetime

# MongoDB connection setup
client = MongoClient(uri)
db = client[dbname]
collection = db[collection_name]

# List of symbols
symbols = ["MC.PA", "RMS.PA", "OR.PA", "CDI.PA", "TTE.PA", "AIR.PA", "SU.PA", "SAN.PA", "AI.PA", "EL.PA", "SAF.PA", "CS.PA", "DG.PA", "BNP.PA", "DSY.PA", "KER.PA", "BN.PA"]

# CSV file setup
csv_file_path = 'bourses/historical_data.csv'
csv_columns = ['_id', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbole']

# Writing to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    
    for symbol in symbols:
        documents = collection.find({"Symbole": symbol})
        for document in documents:
            document.pop('_id', None)
            writer.writerow(document)

print(f"Data successfully written to {csv_file_path}")
