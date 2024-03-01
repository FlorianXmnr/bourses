import pandas as pd

url = "https://live.euronext.com/markets/paris/equities/list"

try:
    # Lire toutes les tables dans la page web
    df_list = pd.read_html(url)

    # Initialiser une liste vide pour stocker tous les symboles
    liste_symboles = []

    # Compiler tous les symboles de chaque table (si plusieurs)
    for df in df_list:
        # Assurez-vous que 'Symbol' est une colonne dans le DataFrame
        if 'Symbol' in df.columns:
            liste_symboles.extend(df['Symbol'].tolist())

    # Afficher la liste complète des symboles
    print(liste_symboles)
except Exception as e:
    print("Erreur lors de l'extraction des données :", e)
