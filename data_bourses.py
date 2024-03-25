import streamlit as st
import pandas as pd

from sklearn.linear_model import LinearRegression

import numpy as np
from pandas.tseries.offsets import BDay

from datetime import datetime, timedelta

st.title("Mon Application Streamlit")

# Lire le fichier CSV dans un DataFrame
df = pd.read_csv('data/historical_data.csv', sep=";")
df_crypto = pd.read_csv('data/historical_data_crypto.csv', sep=";")

# Liste des options pour les "onglets"
tabs = ["Bourses", "Cryptomonnaies", "Prédictions"]

# Créer les "onglets" avec des boutons radio
tab = st.radio("Choisissez un onglet:", tabs)

# Afficher le contenu en fonction de l'onglet sélectionné
if tab == "Bourses":
    # Récupérer les données de la colonne 'Symbole'
    symboles = df['Symbole'].unique()
    options = ['Open', 'Low', 'High', 'Close']

    # Créer la liste déroulante
    selection = st.selectbox('Choisissez une option:', symboles)
    bourses = st.selectbox("Choisissez une période: ", options)

    # Filtrer le DataFrame en fonction de la sélection de l'utilisateur
    filtered_df = df[df['Symbole'] == selection]

    # Définir 'Date' comme index
    filtered_df.set_index('Date', inplace=True)

    # Créer le graphique
    st.line_chart(filtered_df[bourses])
elif tab == "Cryptomonnaies":
    # Récupérer les données de la colonne 'Symbole'
    symboles = df_crypto['Symbole'].unique()
    options = ['Open', 'Low', 'High', 'Close']

    # Créer la liste déroulante
    selection = st.selectbox('Choisissez une option:', symboles)
    bourses = st.selectbox("Choisissez une période: ", options)

    # Filtrer le DataFrame en fonction de la sélection de l'utilisateur
    filtered_df = df_crypto[df_crypto['Symbole'] == selection]

    # Définir 'Date' comme index
    filtered_df.set_index('Date', inplace=True)

    # Créer le graphique
    st.line_chart(filtered_df[bourses])
elif tab == "Prédictions":
    # Créer un DataFrame vide pour les prédictions
    df_predictions = pd.DataFrame(
        columns=['Symbole', 'Dernière Close', 'Date ATH', 'ATH', 'Période ATH', 'Tendance', 'Prediction J+30',
                 'Evolution attendue'])

    # Pour chaque symbole d'action
    for symbol in df['Symbole'].unique():
        # Filtrer le DataFrame pour le symbole actuel
        df_symbol = df[df['Symbole'] == symbol]

        # Convertir la colonne de date en datetime
        df_symbol['Date'] = pd.to_datetime(df_symbol['Date'])
        start_date = pd.to_datetime('2024-02-05')
        df_symbol = df_symbol[df_symbol['Date'] >= start_date]

        # Extraire le nombre de jours et créer une nouvelle colonne 'Days'
        df_symbol['Days'] = (df_symbol['Date'] - df_symbol['Date'].min()) / np.timedelta64(1, 'D')

        # Définir X et y
        X = df_symbol['Days'].values.reshape(-1, 1)
        y = df_symbol['Close'].values.reshape(-1, 1)

        # Entraîner le modèle
        regressor = LinearRegression()
        regressor.fit(X, y)

        # Définir la date de début pour les prévisions, en excluant les week-ends
        start_forecast_date = pd.to_datetime('2024-03-21')

        # Calculer le nombre de jours ouvrables à prédire
        days_in_future = 31  # Le nombre total de jours à prédire
        future_business_days = pd.date_range(start_forecast_date, periods=days_in_future, freq=BDay())

        # Convertir les dates futures en nombres, basé sur le calcul original
        future_forecast_days = [(day - start_date).days for day in future_business_days]
        future_forecast = np.array(future_forecast_days).reshape(-1, 1)

        # Prédiction avec le modèle entraîné
        y_pred = regressor.predict(future_forecast)

        # Calculer la date de l'ATH et la période de l'ATH
        ath_date = df_symbol.loc[df_symbol['Close'].idxmax(), 'Date']
        today = datetime.today()

        if today - ath_date <= timedelta(days=90):
            ath_period = 'Récent (-3mois)'
        elif timedelta(days=90) < today - ath_date <= timedelta(days=365):
            ath_period = 'Moins d\'un an'
        else:
            ath_period = 'Plus d\'un an'

        # Dernière donnée réelle
        last_real_data = df_symbol['Close'].iloc[-1]

        # Dernière donnée prédictive
        last_predicted_data = y_pred[-1]

        # Déterminer la tendance
        if last_real_data < last_predicted_data:
            trend = 'Haussière'
        else:
            trend = 'Baissière'

        # Ajouter les prédictions au DataFrame
        new_row = pd.DataFrame({
            'Symbole': [symbol],
            'Dernière Close': [last_real_data],
            'Date ATH': [ath_date],
            'ATH': [df_symbol['Close'].max()],
            'Période ATH': [ath_period],
            'Tendance': [trend],
            'Prediction J+30': [y_pred[30]],  # Remplacer par la prédiction J+30
            'Evolution attendue': [(y_pred[30] - last_real_data) / last_real_data]
        })

        df_predictions = pd.concat([df_predictions, new_row], ignore_index=True)

    # Afficher les prédictions
    st.dataframe(df_predictions)