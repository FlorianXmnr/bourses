import pandas as pd
import matplotlib.pyplot as plt


# Charger les données
df = pd.read_csv('fichiers/Data.csv', sep=";")
df = df[df['Symbole'] == 'CS.PA']
# Supposons que df est votre DataFrame
df['Date'] = pd.to_datetime(df['Date'])

############
"""plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Open'])
plt.title('Open Price Over Time')
plt.xlabel('Date')
plt.ylabel('Open Price')
plt.show()"""


#############
df = df[df["Open"] >= 20]
lignes = df.shape[0]
print(f"Il y a {lignes} jours")

plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Open'])
plt.title('Open Price Over Time')
plt.xlabel('Date')
plt.ylabel('Open Price')
plt.show()
