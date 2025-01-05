import pymongo 
from dotenv import load_dotenv
import os 
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")


mongo_client=pymongo.MongoClient(MONGO_DB_URL)
collection=mongo_client['MK-NetworkSecurity']['NetworkData']
print(list(collection.find()))