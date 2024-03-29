import yfinance as yf

# Créer un objet Ticker
msft = yf.Ticker("MSFT")

# Obtenir toutes les informations sur l'action
info = msft.info

# Obtenir les données historiques du marché
hist = msft.history(interval="30m")

# Obtenir les actions (dividendes, splits, gains en capital)
actions = msft.actions


print(hist)
print(info)