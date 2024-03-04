from pymongo import MongoClient
import os
"""user = "alexiszueraspro"
password = "DJK7hi0GRSkl8upZ"
host = "clusterbourse.60a6vhb.mongodb.net"
dbname = "Stage"
collection_name = "Bourse"""

user = os.environ.get("Secrets.MONGO_USER")
password = os.environ.get("Secrets.MONGO_PASSWORD")
host = os.environ.get("Secrets.MONGO_HOST")
dbname = os.environ.get("Secrets.MONGO_DBNAME")
collection_name = os.environ.get("Secrets.MONGO_COLLECTION_NAME")

print(user)
print(password)
print(host)
print(dbname)
print(collection_name)

uri = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority&appName=ClusterBourse&tls=true"
client = MongoClient(uri)


"""# URI de connexion
uri = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority&appName=ClusterBourse"
# Se connecter à MongoDB
client = MongoClient(uri)"""
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    # Complétez cette liste avec les symboles réels
    symboles = ["MC.PA", "RMS.PA", "OR.PA", "CDI.PA", "TTE.PA", "AIR.PA", "SU.PA", "SAN.PA", "AI.PA", "EL.PA", "SAF.PA",
                "CS.PA", "DG.PA", "BNP.PA", "DSY.PA", "KER.PA",
                "BN.PA"]
except Exception as e:
    print(e)


