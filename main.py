import yfinance as yf

# Remplacer 'BN.PA' par le symbole de votre choix
symbole = 'BN.PA'  # Exemple pour BNP Paribas, cotée sur Euronext Paris
action = yf.Ticker(symbole)

# Récupérer les données historiques
historique = action.history(period="max")  # 'max' pour l'historique complet, ou '1mo', '1y', etc.

# Réinitialiser l'index pour transformer les dates d'index en une colonne "Date"
historique_reset = historique.reset_index()

# Afficher les premières lignes pour vérifier
print(historique_reset.head())

historique_reset.to_csv('donnees_historiques.csv', index=False,sep=";", date_format="%d/%m/%Y")