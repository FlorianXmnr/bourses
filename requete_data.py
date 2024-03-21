from scipy import stats
from pandas.tseries.offsets import BDay
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
import pandas as pd
import numpy as np
import time

df = pd.read_csv('data/historical_data.csv', sep=";")
df = df[df['Symbole'] == 'KER.PA']
# Convertir la colonne de date en datetime et extraire le nombre de jours
df['Date'] = pd.to_datetime(df['Date'])
start_date = pd.to_datetime('2023-02-01')
df = df[df['Date'] >= start_date]
df['Date'] = (df['Date'] - df['Date'].min()) / np.timedelta64(1, 'D')

# Définir X et y
X = df['Date'].values.reshape(-1, 1)
y = df['Close'].values.reshape(-1, 1)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Liste des algorithmes à évaluer
algos = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(),
    "Support Vector Regression": SVR(),
    "Gradient Boosting": GradientBoostingRegressor(),
    "XGBoost": XGBRegressor(),
    "Ridge Regression": Ridge(),
    "Lasso Regression": Lasso(),
    "Elastic Net": ElasticNet(),
    "Gaussian Process": GaussianProcessRegressor(),
    "Decision Tree": DecisionTreeRegressor(),
    "K-Nearest Neighbors": KNeighborsRegressor(),
    "Multilayer Perceptron": MLPRegressor(),
    "AdaBoost": AdaBoostRegressor()
}
results = []
# Effectuer le benchmark
for name, algo in algos.items():
    # Enregistrer le temps de début
    start_time = time.time()

    # Entraîner l'algorithme
    model = algo.fit(X_train, y_train.ravel())  # Utilisez ravel() pour convertir y en 1D

    # Calculer le temps d'entraînement
    training_time = time.time() - start_time

    # Faire des prédictions sur l'ensemble de test
    predictions = model.predict(X_test)

    # Calculer le score R^2
    r2_score = metrics.r2_score(y_test, predictions)
    # Ajouter les résultats à la liste
    results.append({
        'Algorithme': name,
        'R^2 Score': r2_score,
        'Temps d\'entraînement': training_time
    })

# Créer un DataFrame à partir des résultats
df_results = pd.DataFrame(results)

# Trier le DataFrame par score R^2 en descendant
df_results = df_results.sort_values(by='R^2 Score', ascending=False)

# Afficher le classement
print(df_results)

# Entraîner le modèle
model = RandomForestRegressor().fit(X_train, y_train.ravel())

start_forecast_date = pd.to_datetime('2024-03-21')

# Calculer le nombre de jours ouvrables à prédire
days_in_future = 30  # Le nombre total de jours à prédire
future_business_days = pd.date_range(start_forecast_date, periods=days_in_future, freq=BDay())
predictions = []
# Convertir les dates futures en nombres, basé sur le calcul original
future_forecast_days = [(day - (start_date + pd.Timedelta(days=df['Date'].min()))).days for day in future_business_days]
future_forecast = np.array(future_forecast_days).reshape(-1, 1)

for i in range(days_in_future):
    if i == 0:
        # Utiliser la dernière valeur de l'ensemble d'entraînement pour la première prédiction
        input_data = X_train[-1].reshape(1, -1)
    else:
        # Utiliser la prédiction précédente pour la prochaine prédiction
        input_data = np.array([[predictions[-1]]])

    # Faire une prédiction et l'ajouter à la liste des prédictions
    prediction = model.predict(input_data)
    predictions.append(prediction[0])

# Création d'un DataFrame pour les prédictions futures
future_predictions_df = pd.DataFrame({
    'Future Date': future_business_days,
    'Predicted Close': predictions
})

# Afficher les prédictions
print(future_predictions_df.head(10))

residuals = y_test - model.predict(X_test)

# Calculer l'erreur standard des résidus
stderr = residuals.std()

# Nombre de prédictions
n = future_forecast.shape[0]

# Degrés de liberté
df = len(X_test) - 2
print(df)
# Trouver le t-score pour un intervalle de confiance de 95%
t_score = stats.t.ppf(0.975, df)

# Calculer l'intervalle de confiance pour chaque prédiction
confidence_interval = t_score * stderr / np.sqrt(n)

# Ajouter l'intervalle de confiance aux prédictions
future_predictions_df['Lower Bound'] = future_predictions_df['Predicted Close'] - confidence_interval
future_predictions_df['Upper Bound'] = future_predictions_df['Predicted Close'] + confidence_interval

# Afficher les prédictions avec l'intervalle de confiance
print(future_predictions_df.head(10))

# Entraîner le modèle sur toutes les données disponibles
model = DecisionTreeRegressor().fit(X, y.ravel())

start_forecast_date = pd.to_datetime('2024-03-21')

# Calculer le nombre de jours ouvrables à prédire
days_in_future = 30  # Le nombre total de jours à prédire
future_business_days = pd.date_range(start_forecast_date, periods=days_in_future, freq=BDay())

future_forecast_days = [(day - start_date).days if day != start_date else 0 for day in future_business_days]
future_forecast = np.array(future_forecast_days).reshape(-1, 1)

# Prédiction avec le modèle entraîné
y_pred = model.predict(future_forecast)

# Création d'un DataFrame pour les prédictions futures
future_predictions_df = pd.DataFrame({
    'Future Date': future_business_days,
    'Predicted Close': y_pred
})

# Afficher les prédictions
print(future_predictions_df.head(10))

residuals = y_test - model.predict(X_test)

# Calculer l'erreur standard des résidus
stderr = residuals.std()

# Nombre de prédictions
n = future_forecast.shape[0]

# Degrés de liberté
df = len(X_test) - 2
print(df)
# Trouver le t-score pour un intervalle de confiance de 95%
t_score = stats.t.ppf(0.975, df)

# Calculer l'intervalle de confiance pour chaque prédiction
confidence_interval = t_score * stderr / np.sqrt(n)

# Ajouter l'intervalle de confiance aux prédictions
future_predictions_df['Lower Bound'] = future_predictions_df['Predicted Close'] - confidence_interval
future_predictions_df['Upper Bound'] = future_predictions_df['Predicted Close'] + confidence_interval

# Afficher les prédictions avec l'intervalle de confiance
print(future_predictions_df.head(10))
