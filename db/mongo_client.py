from pymongo import MongoClient
from film_logger import logger_decorator

class MongoDB:
    @logger_decorator
    def __init__(self, config):
        self.client = MongoClient(config["uri"])
        self.db = self.client[config["database"]]
        self.collection = self.db[config["collection"]]


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def ping(self):
        return self.client.admin.command("ping")


    @logger_decorator
    def close(self):
        self.client.close()


    @logger_decorator
    def log(self, doc):
        return self.collection.insert_one(doc)