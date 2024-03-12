import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from keras import regularizers
import matplotlib.pyplot as plt


# Charger les données
df = pd.read_csv('Data.csv', sep=";")
df = df[df['Symbole'] == 'KER.PA']
# Convertir la colonne de date en datetime et extraire le nombre de jours
df['Date'] = pd.to_datetime(df['Date'])
start_date = pd.to_datetime('2023-02-01')
df = df[df['Date'] >= start_date]
df['Date'] = (df['Date'] - df['Date'].min()) / np.timedelta64(1, 'D')

# Définir X et y
X = df['Date'].values.reshape(-1, 1)
y = df['Close'].values.reshape(-1, 1)

# Diviser les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Créer un modèle séquentiel
model = Sequential()

# Ajouter des couches cachées avec régularisation L1 et L2
model.add(Dense(1024, input_dim=1, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)))
model.add(Dense(512, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)))
model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)))
model.add(Dense(128, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)))
model.add(Dense(64, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)))
model.add(Dense(32, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)))
model.add(Dense(32, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)))
model.add(Dense(32, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)))
model.add(Dense(32, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.01)))

# Ajouter une couche de sortie avec 1 neurone (puisque nous faisons de la régression)
model.add(Dense(1))

# Compiler le modèle
model.compile(loss='mean_squared_error', optimizer='adam')

# Entraîner le modèle avec plus d'époques
model.fit(X_train, y_train, epochs=150, batch_size=5, verbose=0)

# Évaluer le modèle
train_loss = model.evaluate(X_train, y_train, verbose=0)
test_loss = model.evaluate(X_test, y_test, verbose=0)

print(f'Train Loss: {train_loss}')
print(f'Test Loss: {test_loss}')
"""
# Définir le nombre de jours à prédire
num_days = 60

# Créer un array contenant les valeurs des jours pour lesquels faire des prédictions
last_day = X_train.max()
X_pred = np.linspace(last_day, last_day + num_days, num_days).reshape(-1, 1)

# Faire des prédictions
y_pred = model.predict(X_pred)
print(X_pred)
print(y_pred)
# Afficher les prédictions
plt.figure(figsize=(10, 5))
plt.plot(X_pred, y_pred, 'r-', label='Prédictions')
plt.xlabel('Jours')
plt.ylabel('Prix de clôture')
plt.title('Prédictions des prix de clôture pour les prochains jours')
plt.legend()
plt.show()"""