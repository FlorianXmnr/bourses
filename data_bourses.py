import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go

st.title("Mon Application Streamlit")

# Lire le fichier CSV dans un DataFrame
df = pd.read_csv('data/historical_data.csv', sep=";")
df_crypto = pd.read_csv('data/historical_data_crypto.csv', sep=";")

# Liste des options pour les "onglets"
tabs = ["Bourses", "Cryptomonnaies", "Prédictions","Présentation Boursière (type chandeliers japonais)"]

# Créer les "onglets" avec des boutons radio
tab = st.radio("Choisissez un onglet:", tabs)

# Dictionnaire qui mappe les symboles aux noms des entreprises
symbole_to_nom = {
        "LVMH Moët Hennessy - Louis Vuitton": "MC.PA",
        "Hermès International Société": "RMS.PA",
        "L'Oréal S.A.": "OR.PA",
        "Christian Dior SE": "CDI.PA",
        "TotalEnergies SE": "TTE.PA",
        "Airbus SE": "AIR.PA",
        "Schneider Electric S.E.": "SU.PA",
        "Sanofi": "SAN.PA",
        "L'Air Liquide S.A.": "AI.PA",
        "EssilorLuxottica Société anonyme": "EL.PA",
        "Safran SA": "SAF.PA",
        "AXA SA": "CS.PA",
        "Vinci SA": "DG.PA",
        "BNP Paribas SA": "BNP.PA",
        "Dassault Systèmes SE": "DSY.PA",
        "Kering SA": "KER.PA",
        "Danone S.A.": "BN.PA"
}

crypto_to_symbole = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Tether": "USDT-USD",
    "Binance Coin": "BNB-USD",
    "Solana": "SOL-USD",
    "Lido Staked ETH": "STETH-USD",
    "Ripple": "XRP-USD",
    "USD Coin": "USDC-USD",
    "Cardano": "ADA-USD",
    "Dogecoin": "DOGE-USD",
    "Avalanche": "AVAX-USD",
    "Shiba Inu": "SHIB-USD"
}


# Afficher le contenu en fonction de l'onglet sélectionné
if tab == "Bourses":
    # Créer la liste déroulante avec les noms des entreprises
    symboles = df['Symbole'].unique()
    options = ['Open', 'Low', 'High', 'Close']
    # Utilisez directement les clés du dictionnaire pour la sélection
    selection_nom = st.selectbox('Choisissez une entreprise:', list(symbole_to_nom.keys()))
    bourses_option = st.selectbox("Choisissez une période: ", options)

    # Récupérer le symbole correspondant au nom de l'entreprise sélectionnée
    symbole_selectionne = symbole_to_nom[selection_nom]

    # Filtrer le DataFrame en fonction du symbole sélectionné
    filtered_df = df[df['Symbole'] == symbole_selectionne]

    # Assurez-vous que 'Date' est au format datetime et définissez-le comme index
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    filtered_df.set_index('Date', inplace=True)

    # Vérifier si l'utilisateur a sélectionné une période et afficher le graphique correspondant
    if bourses_option:
        st.line_chart(filtered_df[bourses_option])
elif tab == "Cryptomonnaies":
    # Liste déroulante pour choisir une cryptomonnaie
    selection_cryptomonnaie = st.selectbox('Choisissez une cryptomonnaie:', list(crypto_to_symbole.keys()))

    # Liste déroulante pour choisir une période
    periode_options = ['Open', 'Low', 'High', 'Close']
    periode_selectionnee = st.selectbox("Choisissez une période: ", periode_options)

    # Filtrer le DataFrame en fonction de la cryptomonnaie sélectionnée
    symbole_selectionne = crypto_to_symbole[selection_cryptomonnaie]
    filtered_df_crypto = df_crypto[df_crypto['Symbole'] == symbole_selectionne]

    # Assurez-vous que 'Date' est au format datetime et définissez-la comme index
    filtered_df_crypto['Date'] = pd.to_datetime(filtered_df_crypto['Date'])
    filtered_df_crypto.set_index('Date', inplace=True)

    # Afficher le graphique pour la période sélectionnée
    st.line_chart(filtered_df_crypto[periode_selectionnee])
elif tab == "Prédictions":
    # Charger le fichier CSV dans un DataFrame
    df["Date"] = pd.to_datetime(df["Date"])

    # Trier le DataFrame par la colonne de dates
    df_tri = df.sort_values(by=['Symbole', 'Date'])
    # Reformater la colonne 'Date' au format jour/mois/année

    # Sélectionner la dernière valeur de 'Close' pour chaque symbole
    last_close_df = df_tri.groupby('Symbole')['Close'].last().reset_index()
    # Renommer la colonne pour correspondre à votre demande
    last_close_df = last_close_df.rename(columns={'Close': 'Dernière Close'})

    print(last_close_df)

    # Sélectionner la valeur maximale de 'Close' pour chaque symbole avec la date associée
    ath_df = df_tri.loc[df_tri.groupby('Symbole')['Close'].idxmax()][['Symbole', 'Date', 'Close']]
    ath_df = ath_df.rename(columns={'Close': 'ATH'})
    print(ath_df)

    # Fusionner les deux DataFrames sur la colonne 'Symbole'
    result_df = pd.merge(last_close_df, ath_df, on='Symbole')

    # Ajouter une nouvelle colonne avec la dernière date du DataFrame df_tri pour chaque symbole
    last_date_tri_df = df_tri.groupby('Symbole')['Date'].last().reset_index()
    last_date_tri_df = last_date_tri_df.rename(columns={'Date': 'Fermeture'})
    result_df = pd.merge(result_df, last_date_tri_df, on='Symbole')

    # Convertir les colonnes 'Fermeture' et 'Date' en objets datetime
    result_df['Fermeture'] = pd.to_datetime(result_df['Fermeture'], format='%d/%m/%Y')
    result_df['Date'] = pd.to_datetime(result_df['Date'], format='%d/%m/%Y')

    # Ajouter une nouvelle colonne avec la différence de jours
    result_df['Diff_Jours'] = (result_df['Fermeture'] - result_df['Date']).dt.days

    # Définir les conditions
    recent_condition = (result_df['Diff_Jours'] <= 90)
    moins_un_an_condition = ((result_df['Diff_Jours'] > 90) & (result_df['Diff_Jours'] <= 365))

    # Appliquer les conditions et créer la nouvelle colonne
    result_df['Periode'] = 'Plus d\'un an'
    result_df.loc[recent_condition, 'Periode'] = 'Récent (-3mois)'
    result_df.loc[moins_un_an_condition, 'Periode'] = 'Moins d\'un an'
    result_df = result_df.drop(columns=['Fermeture', 'Diff_Jours'])
    print(result_df)

    # Paramètres
    start_date = pd.to_datetime('01/01/2024', format='%d/%m/%Y')  # Date de début du modèle
    start_forecast_date = pd.Timestamp.now()  # Date de début des prédictions
    days_to_forecast = 30  # Nombre de jours à prédire

    # Convertir la colonne 'Date' en objets de date
    df_tri['Date'] = pd.to_datetime(df_tri['Date'])

    print(df_tri)

    # Créer une colonne pour stocker les prédictions
    result_df['Estimation J+30'] = np.nan

    # Pour chaque symbole, entraîner le modèle et prédire les valeurs 30 jours plus tard
    for symbole in result_df['Symbole']:
        # Filtrer les données correspondant à chaque symbole
        symbole_data = df_tri[df_tri['Symbole'] == symbole]

        # Sélectionner les données jusqu'à la date de début du modèle
        df_train = symbole_data[symbole_data['Date'] >= start_date]

        # Extraire les variables indépendantes (X) et dépendantes (y)
        X = (df_train['Date'] - start_date) / np.timedelta64(1, 'D')
        X = X.values.reshape(-1, 1)
        y = df_train['Close'].values.reshape(-1, 1)

        # Entraîner le modèle de régression linéaire
        regressor = LinearRegression()
        regressor.fit(X, y)

        # Calculer la pente de la régression linéaire
        slope = regressor.coef_[0][0]

        # Déterminer la tendance en fonction de la pente
        trend = "Haussière" if slope > 0 else "Baissière"

        # Ajouter la tendance à la dataframe result_df
        result_df.loc[result_df['Symbole'] == symbole, 'Tendance'] = trend

        # Prédire les valeurs 30 jours plus tard
        future_date = start_forecast_date + pd.DateOffset(days=days_to_forecast)
        future_value = regressor.predict(np.array((future_date - start_date).days).reshape(1, -1))

        # Ajouter la prédiction à result_df
        result_df.loc[result_df['Symbole'] == symbole, 'Prediction J+30'] = future_value
        print(result_df)

    # Estimation de rendement en pourcentage
    estimation = ((result_df['Prediction J+30'] - result_df['Dernière Close']) / result_df['Dernière Close']) * 100
    estimation = estimation.map("{:.2f}%".format)

    # Ajout de la colonne "Evolution attendue" à result_df
    result_df['Evolution attendue'] = estimation
    result_df = result_df.drop(columns=['Estimation J+30'])

    # Renommer la colonne "Date" en "Date ATH"
    result_df = result_df.rename(columns={'Date': 'Date ATH'})
    # Afficher les prédictions
    st.dataframe(result_df)
elif tab == "Présentation Boursière (type chandeliers japonais)":
    # Récupérer les symboles uniques
    symboles = df['Symbole'].unique()

    # Créer une liste déroulante pour la sélection du symbole
    selection = st.selectbox('Choisissez une option:', symboles)

    # Filtrer le DataFrame en fonction de la sélection de l'utilisateur
    filtered_df = df[df['Symbole'] == selection]

    # Assurez-vous que votre DataFrame contient les colonnes 'Open', 'High', 'Low', 'Close' et 'Date'
    if {'Open', 'High', 'Low', 'Close', 'Date'}.issubset(filtered_df.columns):
        # Convertir la colonne 'Date' en datetime
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

        # Créer un graphique en chandelier
        fig = go.Figure(data=[go.Candlestick(x=filtered_df['Date'],
                                             open=filtered_df['Open'],
                                             high=filtered_df['High'],
                                             low=filtered_df['Low'],
                                             close=filtered_df['Close'])])

        # Afficher le graphique sur Streamlit
        st.plotly_chart(fig)
    else:
        st.write("Votre DataFrame ne contient pas les colonnes nécessaires.")
