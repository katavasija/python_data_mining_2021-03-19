import pymongo


class MongoHelper:
    MONGO_URL = 'mongodb://localhost:27017'

    def __init__(self, db_name='gb_parse_19_03_21'):
        client = pymongo.MongoClient(self.MONGO_URL)
        self.db = client[db_name]

    def save(self, data, collection_name='magnit'):
        collection = self.db[collection_name]
        collection.insert_one(data)
