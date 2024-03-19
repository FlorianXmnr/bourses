import pandas as pd
import matplotlib.pyplot as plt


# Charger les données
df = pd.read_csv('data/historical_data.csv', sep=";")
df_crypto = pd.read_csv('data/historical_data_crypto.csv', sep=";")
df = df[df['Symbole'] == 'CS.PA']
# Supposons que df est votre DataFrame
df['Date'] = pd.to_datetime(df['Date'])

plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Open'])
plt.title('Open Price Over Time')
plt.xlabel('Date')
plt.ylabel('Open Price')
plt.show()


