from pymongo import MongoClient

user = "alexiszueraspro"
password = "DJK7hi0GRSkl8upZ"
host = "clusterbourse.60a6vhb.mongodb.net"
dbname = "Stage"
collection_name = "Bourse"

# URI de connexion
uri = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority&appName=ClusterBourse"
# Se connecter à MongoDB
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


