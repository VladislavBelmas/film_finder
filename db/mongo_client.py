from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from film_logger import logger_decorator

class MongoDB:
    @logger_decorator
    def __init__(self, config):
        self.client = MongoClient(config["uri"], serverSelectionTimeoutMS=2000)
        self.db = self.client[config["database"]]
        self.collection = self.db[config["collection"]]


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_connected():
            self.close()


    def is_connected(self):
        try:
            self._ping()
            return True
        except ConnectionFailure:
            return False


    @logger_decorator
    def close(self):
        self.client.close()


    @logger_decorator
    def log(self, doc):
        return self.collection.insert_one(doc)

    @logger_decorator
    def get_logs(self, filter_query=None, limit=100):
        if filter_query is None:
            filter_query = {}
        return list(self.collection.find(filter_query).limit(limit).sort("_id", -1))


    def _ping(self):
        return self.client.admin.command("ping")
