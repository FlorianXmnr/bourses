import matplotlib.dates as mdates
from API.connection import *
import pandas as pd
import matplotlib.pyplot as plt


db = client[dbname]
collection = db[collection_name]

# Example query: Retrieve historical data for a specific symbol
symbol = "MC.PA"  # Example symbol

# Retrieve all documents for this symbol
documents = list(collection.find({"Symbole": symbol}))

# Convert to DataFrame for analysis
df = pd.DataFrame(documents)
# Supposons que df est votre DataFrame
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

print(df.dtypes)

selected_columns = df.loc[:, "Open":"Volume"]

# Use the .describe() method to get the summary statistics
description = selected_columns.describe()

print(description)

plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Open'])
plt.title('Open Price Over Time')
plt.xlabel('Date')
plt.ylabel('Open Price')

# Formatage de l'axe des x pour afficher uniquement le mois et l'année
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.gcf().autofmt_xdate() # Rotation automatique des dates pour une meilleure lisibilité

plt.savefig('open_price_plot.png')
