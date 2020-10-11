import os
import pymongo
import os

# initialize the mongodb client
client = pymongo.MongoClient(os.getenv("MONGO_DB"))

class DB:
    @staticmethod
    async def store_data(data):
        try:
            db = client['Covid19PH_Data']
            collection = db["datas"]

            # insert the data
            collection.insert_one(data)

        except Exception:
            return False


        return True