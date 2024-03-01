from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Configuration de Selenium avec ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Ouvrir la page web
driver.get("https://live.euronext.com/markets/paris/equities/list")

time.sleep(10)  # Attendre que le JavaScript soit chargé

# Récupérer le HTML de la page après exécution du JavaScript
html = driver.page_source

# Fermer le navigateur
driver.quit()

# Analyser le HTML avec pandas
dfs = pd.read_html(html)

# Rechercher dans chaque DataFrame pour trouver celui contenant les symboles
for df in dfs:
    if 'Symbol' in df.columns:
        print(df['Symbol'])
