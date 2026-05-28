import pymysql
from collections.abc import Iterable


class MySql:
    def __init__(self, config):
        self.connection = pymysql.connect(**config)


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


    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.connection.close()


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

        if not isinstance(params, Iterable) or isinstance(params, str):
            raise TypeError("Должно быть итерируемым и не строкой")

