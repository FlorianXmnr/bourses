from connection_crypto import *
import csv

# MongoDB connection setup
client = MongoClient(uri)
db = client[dbname]
collection = db[collection_name_crypto]

# CSV file setup

csv_directory = "data"
os.makedirs(csv_directory, exist_ok=True)

csv_file_path = os.path.join(csv_directory, "historical_data.csv")
csv_columns = ['_id', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Symbole']
# Proceed with writing to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=";")
    writer.writeheader()

    for symbol in symboles:
        documents = collection.find({"Symbole": symbol}).sort([("Symbole", 1), ("Date", 1)])
        for document in documents:
            document.pop('_id', None)
            writer.writerow(document)


print(f"Data successfully written to {csv_file_path}")
