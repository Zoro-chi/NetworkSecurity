import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import dotenv
import pymongo

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

# Load the .env file
dotenv.load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
certificate_authority = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def convert_csv_to_json(self, file_path):
        try:
            df = pd.read_csv(file_path)
            # Drop index
            df.reset_index(drop=True, inplace=True)
            # Convert to json
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database_name, collection_name):
        try:
            self.database_name = database_name
            self.collection_name = collection_name
            self.records = records

            self.mongo_client = pymongo.MongoClient(
                MONGODB_URI, tlsCAFile=certificate_authority
            )
            self.database = self.mongo_client[self.database_name]
            self.collection = self.database[self.collection_name]

            # Insert data
            self.collection.insert_many(self.records)
            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "Phising_Data_Science"
    Collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.convert_csv_to_json(FILE_PATH)
    no_of_records = networkobj.insert_data_to_mongodb(records, DATABASE, Collection)
    print(f"Inserted {no_of_records} records to MongoDB")
