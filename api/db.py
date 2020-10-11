import os
import pymongo
import os

# initialize the mongodb client
client = pymongo.MongoClient(os.getenv("MONGO_DB"))

class DB:
    db = client['Covid19PH_Data']
    collection = db["datas"]

    @staticmethod
    async def store_data(data):
        try:
            # insert the data
            DB.collection.insert_one(data)

        except Exception:
            return False


        return True

    @staticmethod
    async def get_data(case_name=False):
        cursor = DB.collection.find().sort("crawl_time", -1).limit(1)

        data = {}

        for i in cursor: data = i

        if case_name:
            return data["data"][case_name]

        return data