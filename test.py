import pandas as pd
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression


# Lire le fichier CSV dans un DataFrame
df = pd.read_csv('data/historical_data.csv', sep=";")
df_crypto = pd.read_csv('data/historical_data_crypto.csv', sep=";")

# Convertir la colonne 'Date' en datetime
df['Date'] = pd.to_datetime(df['Date'])
df_crypto['Date'] = pd.to_datetime(df_crypto['Date'])

# Créer un DataFrame vide pour les ATH
df_ath = pd.DataFrame(columns=['Symbole', 'Dernière Close', 'Date ATH', 'ATH', 'Période ATH'])


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
        n_days = 30  # nombre de jours à utiliser pour calculer la tendance
        X_trend = np.array(range(n_days)).reshape(-1, 1)  # jours
        y_trend = df_symbol['Close'].values[-n_days:]  # prix de clôture des n derniers jours
        trend_model = LinearRegression()
        trend_model.fit(X_trend, y_trend)
        slope = trend_model.coef_

        if slope > 0:
            trend = 'Haussière'
        else:
            trend = 'Baissière'

        # Ajouter l'ATH, la date de l'ATH, la période de l'ATH et la prédiction à df_ath
        new_row = pd.DataFrame({
            'Symbole': [f"{symbol} ({df_name})"],
            'Dernière Close': [last_close],
            'Date ATH': [ath_date],
            'ATH': [ath],
            'Période ATH': [ath_period]
        })

        df_ath = pd.concat([df_ath, new_row], ignore_index=True)

# Afficher df_ath
print(df_ath)