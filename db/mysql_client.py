import pymysql
from film_logger import logger_decorator

class MySql:
    @logger_decorator
    def __init__(self, config):
        self.connection = pymysql.connect(**config)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    @logger_decorator
    def select(self, query, params=None):
        """
        Выполняет SQL запрос.

        Если запрос возвращает данные (например SELECT),
        возвращает результат fetchall().

        :param query: SQL запрос
        :param params: параметры SQL запроса
        :return:
             список строк результата
        """
        self._params_check(params)

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()


    @logger_decorator
    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.connection.close()


    def ping(self):
        self.connection.ping(reconnect=True)


    @staticmethod
    def _params_check(params):
        """
        Проверяет корректность параметров SQL запроса.

        :param params: параметры SQL запроса
        :raises ValueError:
            если params не является iterable
            или является строкой
        """
        if params is None:
            return

        if not isinstance(params, (tuple, list)):
            raise TypeError("Параметры должны быть tuple или list")

