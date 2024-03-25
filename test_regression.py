import pandas as pd
from datetime import datetime, timedelta

# Lire le fichier CSV dans un DataFrame
df = pd.read_csv('data/historical_data.csv', sep=";")

# Convertir la colonne 'Date' en datetime
df['Date'] = pd.to_datetime(df['Date'])

# Créer une liste pour stocker les données
data = []

# Pour chaque symbole unique dans le DataFrame
for symbol in df['Symbole'].unique():
    # Filtrer les données pour ce symbole
    symbol_data = df[df['Symbole'] == symbol]

    # Trouver l'index de la valeur maximale pour la colonne 'Close'
    max_close_index = symbol_data['Close'].idxmax()

    # Ajouter la ligne correspondante à la liste
    row = df.loc[max_close_index, ['Symbole', 'Close', 'Date']]
    row['Dernière Close'] = symbol_data['Close'].iloc[-1]  # Ajouter la valeur de 'Dernière Close'
    row['ATH'] = symbol_data['Close'].max()  # Ajouter la valeur de 'ATH'
    data.append(row)

# Créer une nouvelle DataFrame à partir de la liste
df_ath = pd.concat(data, axis=1).T.reset_index(drop=True)


# Créer une fonction pour déterminer la période ATH
def determine_period_ath(row):
    if row['Date'] >= datetime.now() - timedelta(days=90):
        return 'Récent (-3 mois)'
    elif row['Date'] >= datetime.now() - timedelta(days=365):
        return 'Moins d\'un an'
    else:
        return 'Plus d\'un an'

def determine_tendance(row):
    if row['ATH'] > row['Dernière Close']:
        return 'Baissière'
    else:
        return 'Haussière'


# Appliquer la fonction à la colonne 'Date' pour créer la colonne 'Période ATH'
df_ath['Période ATH'] = df_ath.apply(determine_period_ath, axis=1)
# Appliquer la fonction aux colonnes 'ATH' et 'Dernière Close' pour créer la colonne 'Tendance'
df_ath['Tendance'] = df_ath.apply(determine_tendance, axis=1)

# Afficher la nouvelle DataFrame
print(df_ath)
