from pymongo import MongoClient


import os

user = os.environ.get("MONGO_USER")
password = os.environ.get("MONGO_PASSWORD")
host = os.environ.get("MONGO_HOST")
dbname = os.environ.get("MONGO_DBNAME")
collection_name = os.environ.get("MONGO_COLLECTION_NAME")

uri = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority&appName=ClusterBourse&tlsInsecure=true"
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    # Complétez cette liste avec les symboles réels
    symboles = ["MC.PA", "RMS.PA", "OR.PA", "CDI.PA", "TTE.PA", "AIR.PA", "SU.PA", "SAN.PA", "AI.PA", "EL.PA", "SAF.PA",
                "CS.PA", "DG.PA", "BNP.PA", "DSY.PA", "KER.PA",
                "BN.PA"]
except Exception as e:
    print(e)


