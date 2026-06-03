import pymysql
from film_logger import logger_decorator

class MySql:
    """MySQL клиент с поддержкой context manager для управления соединением."""

    def __init__(self, config):
        self.config = config


    def __enter__(self):
        self.connection = pymysql.connect(**self.config)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    @logger_decorator
    def select(self, query, params=None):
        """
        Выполняет SQL запрос SELECT.

        :param query: SQL запрос
        :param params: параметры SQL запроса (tuple, list или dict)
        :return: список строк результата
        """
        self._params_check(params)

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


    @logger_decorator
    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection is not None and  self.connection.open:
            self.connection.close()


    def ping(self):
        """Проверяет активность соединения с базой данных."""
        if self.connection is None:
            return False

        try:
            self.connection.ping(reconnect=True)
            return True
        except pymysql.Error:
            return False


    @staticmethod
    def _params_check(params):
        if params is None:
            return

        if not isinstance(params, (tuple, list, dict)):
            raise TypeError("Параметры должны быть tuple, list или dict")

