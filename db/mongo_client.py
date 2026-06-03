from pymongo import MongoClient
from film_logger import logger_decorator

class MongoDB:
    """MongoDB клиент с поддержкой context manager для логирования запросов."""

    def __init__(self, config):
        self.config = config


    def __enter__(self):
        self.client = MongoClient(self.config["uri"], serverSelectionTimeoutMS=2000)
        self.db = self.client[self.config["database"]]
        self.collection = self.db[self.config["collection"]]
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()



    @logger_decorator
    def close(self):
        """Закрывает соединение с MongoDB."""
        if self.client is not None:
            self.client.close()


    @logger_decorator
    def log(self, doc):
        """
        Логирует документ в MongoDB коллекцию.

        :param doc: словарь с данными для логирования
        """
        try:
            self.collection.insert_one(doc)
        except Exception:
            pass


    @logger_decorator
    def get_logs(self, filter_query=None, limit=100):
        """
        Получает логи из MongoDB.

        :param filter_query: фильтр для выборки (по умолчанию None - все документы)
        :param limit: максимальное количество документов
        :return: список документов
        """
        if filter_query is None:
            filter_query = {}
        return list(self.collection.find(filter_query).limit(limit).sort("_id", -1))

