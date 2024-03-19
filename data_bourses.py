import streamlit as st
import pandas as pd

st.title("Mon Application Streamlit")

# Lire le fichier CSV dans un DataFrame
df = pd.read_csv('data/historical_data.csv', sep=";")
df_crypto = pd.read_csv('data/historical_data_crypto.csv', sep=";")

# Liste des options pour les "onglets"
tabs = ["Bourses", "Cryptomonnaies", "Tendances"]

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
else:
    st.write("Vous avez choisi l'onglet 3.")
