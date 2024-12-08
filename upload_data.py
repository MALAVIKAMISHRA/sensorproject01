from pymongo.mongo_client import MongoClient
import pandas as pd
import json

#URL
url = "mongodb+srv://malavika:12345@cluster0.q9tpj.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(url)

# Create database and collection names
DATABASE_NAME = 'pwskills'
COLLECTION_NAME = 'waferfault'

# Corrected file path (use raw string notation)
df = pd.read_csv("C:\Users\MALAVIKA MISHRA\Downloads\sensorproject\notebooks\wafer_23012020_041211.csv")


# Drop the unnamed column
df = df.drop("Unnamed: 0", axis=1)

# Convert dataframe to JSON format (properly convert to list of records)
json_record = list(json.loads(df.T.to_json()).values())

# Insert records into MongoDB
client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
