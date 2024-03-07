import os
from pymongo import MongoClient
import pandas as pd

# Retrieve connection info from environment variables
user = os.environ['MONGO_USER']
password = os.environ['MONGO_PASSWORD']
host = os.environ['MONGO_HOST']
dbname = os.environ['MONGO_DBNAME']
collection_name = os.environ['MONGO_COLLECTION_NAME']

uri = f"mongodb+srv://{user}:{password}@{host}/{dbname}?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client[dbname]
collection = db[collection_name]

# Example query: Retrieve historical data for a specific symbol
symbol = "MC.PA"  # Example symbol

# Retrieve all documents for this symbol
documents = list(collection.find({"Symbole": symbol}))

# Convert to DataFrame for analysis
df = pd.DataFrame(documents)
# Supposons que df est votre DataFrame
print(df.dtypes)
