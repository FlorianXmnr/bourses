from connection_crypto import *
import csv
import pandas as pd
from datetime import *

# MongoDB connection setup
client = MongoClient(uri)
db = client[dbname]
collection = db[collection_name_crypto]

# CSV file setup

csv_directory = "data"
os.makedirs(csv_directory, exist_ok=True)

csv_file_path = os.path.join(csv_directory, "historical_data_crypto.csv")
csv_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbole']
# Proceed with writing to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=";")
    writer.writeheader()

    for symbol in symboles:
        documents = collection.find({"Symbole": symbol}).sort([("Symbole", 1), ("Date", 1)])
        for document in documents:
            document.pop('_id', None)  # Remove the '_id' field
            # Convert the 'Date' field to datetime and format it
            document['Date'] = datetime.strptime(document['Date'], '%d/%m/%Y')
            writer.writerow(document)

# Sort the CSV file by 'Symbole' and 'Date'
df = pd.read_csv(csv_file_path, delimiter=";")
df.sort_values(['Symbole', 'Date'], inplace=True)
df.to_csv(csv_file_path, index=False, sep=";")

print(f"Data successfully written to {csv_file_path}")
