from pymongo import MongoClient
import os

try:

    user = os.environ.get("MONGO_USER")
    password = os.environ.get("MONGO_PASSWORD")
    host = os.environ.get("MONGO_HOST")
    dbname = os.environ.get("MONGO_DBNAME")
    collection_name = os.environ.get("MONGO_COLLECTION_NAME")
    app_name = os.environ.get("MONGO_APP_NAME")
    uri = f"mongodb+srv://{user}:{password}@{host}/{dbname}?retryWrites=true&w=majority&appName={app_name}&tls=true"

    print(uri)
    client = MongoClient(uri)
    symboles = {
        "LVMH Moët Hennessy - Louis Vuitton, Société Européenne": "MC.PA",
        "Hermès International Société en commandite par actions": "RMS.PA",
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
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    # Complétez cette liste avec les symboles réels
except Exception as e:
    print(e)
