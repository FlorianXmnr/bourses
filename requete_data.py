import os
from API.connection import *
import pandas as pd

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

selected_columns = df.loc[:, "Open":"Volume"]

# Use the .describe() method to get the summary statistics
description = selected_columns.describe()

print(description)
