import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from pandas.tseries.offsets import BDay
import numpy as np


# Lire le fichier CSV dans un DataFrame
df = pd.read_csv('data/historical_data.csv', sep=";")
df_crypto = pd.read_csv('data/historical_data_crypto.csv', sep=";")

# Convertir la colonne 'Date' en datetime
df['Date'] = pd.to_datetime(df['Date'])
df_crypto['Date'] = pd.to_datetime(df_crypto['Date'])

# Créer un DataFrame vide pour les ATH
df_ath = pd.DataFrame(columns=['Symbole', 'Dernière Close', 'Date ATH', 'ATH', 'Période ATH', 'Tendance', 'Prédiction J+30'])

# Pour chaque DataFrame
for df_name, df in [('Stocks', df), ('Cryptos', df_crypto)]:
    # Pour chaque symbole d'action
    for symbol in df['Symbole'].unique():
        # Filtrer le DataFrame pour le symbole actuel
        df_symbol = df[df['Symbole'] == symbol]

        # Calculer l'ATH et la date de l'ATH
        ath = df_symbol['Close'].max()
        ath_date = df_symbol.loc[df_symbol['Close'].idxmax(), 'Date']
        # Obtenir la première date dans df_symbol
        start_date = df_symbol['Date'].iloc[0]
        # Calculer la dernière close
        last_close = df_symbol['Close'].iloc[-1]

        # Calculer la période de l'ATH
        today = datetime.today()
        if today - ath_date <= pd.Timedelta(days=90):
            ath_period = 'Récent (-3mois)'
        elif pd.Timedelta(days=90) < today - ath_date <= pd.Timedelta(days=365):
            ath_period = 'Moins d\'un an'
        else:
            ath_period = 'Plus d\'un an'

        # Déterminer la tendance
        if last_close > ath:
            trend = 'Baissière'
        else:
            trend = 'Haussière'

        # Entraîner le modèle de régression linéaire
        X = df_symbol.index.values.reshape(-1,1)
        y = df_symbol['Close'].values.reshape(-1,1)
        model = LinearRegression()
        model.fit(X, y)

        # Prédire la valeur de 'Close' 30 jours ouvrables dans le futur
        last_date = df_symbol['Date'].iloc[-1]

        # Ajouter 30 jours ouvrables à la dernière date
        future_date = last_date + BDay(30)

        # Convertir la future_date en nombre de jours depuis la date de début
        future_day = (future_date - start_date) / np.timedelta64(1, 'D')

        # Prédire la valeur de 'Close' pour future_day
        prediction = model.predict([[future_day]])

        # Ajouter l'ATH, la date de l'ATH, la période de l'ATH et la prédiction à df_ath
        new_row = pd.DataFrame({
            'Symbole': [f"{symbol} ({df_name})"],
            'Dernière Close': [last_close],
            'Date ATH': [ath_date],
            'ATH': [ath],
            'Période ATH': [ath_period],
            'Tendance': [trend],
            'Prédiction J+30': [prediction[0][0]]
        })

        df_ath = pd.concat([df_ath, new_row], ignore_index=True)

# Afficher df_ath
print(df_ath)
