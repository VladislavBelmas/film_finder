from datetime import datetime
from db.mongo_client import MongoDB
from db.mysql_client import MySql
from db.queries import (
    CATEGORIES,
    MIN_FILM_YEAR,
    MAX_FILM_YEAR,
    FILMS,
    FILMS_SPECIFIC_YEAR,
    FILMS_BY_CATEGORY,
    FILMS_BY_ACTOR
)
from film_logger import db_error_handler


class MovieRepository:
    """Репозиторий для работы с данными фильмов из MySQL и логирования в MongoDB."""

    def __init__(self, mysql_db: MySql, mongo_db: MongoDB):
        self.mysql_db = mysql_db
        self.mongo_db = mongo_db


    @db_error_handler(default_return=[])
    def get_categories(self):
        """Возвращает список всех категорий фильмов."""
        return self.mysql_db.select(CATEGORIES)


    @db_error_handler(default_return=(1900, 2026))
    def years_range(self):
        """Возвращает диапазон годов выпуска фильмов в базе (min_year, max_year)."""
        min_year = self.mysql_db.select(MIN_FILM_YEAR)[0]["min_year"]
        max_year = self.mysql_db.select(MAX_FILM_YEAR)[0]["max_year"]
        return min_year, max_year


    @db_error_handler(default_return=[])
    def get_films(self, title="", min_year=0, max_year=9999, limit=10, page=1):
        """
        Поиск фильмов по названию и диапазону лет.

        :param title: Начало названия фильма (пустая строка = все фильмы)
        :param min_year: Минимальный год выпуска
        :param max_year: Максимальный год выпуска
        :param limit: Количество результатов на странице (1-100)
        :param page: Номер страницы (начиная с 1)
        :return: Список словарей с данными фильмов
        """
        pattern, limit, offset = self._default_validator(title, page, limit)
        films = self.mysql_db.select(FILMS, (pattern, min_year, max_year, limit, offset))

        if self.mongo_db:
            self.mongo_db.log({
                "query_type" : "search_by_title",
                "parameters" : {
                    "title": title,
                    "min_year": min_year,
                    "max_year": max_year,
                    "page": page,
                    "limit": limit
                },
                "result_count": len(films),
                "timestamp": datetime.now().isoformat()
            })

        return films


    @db_error_handler(default_return=[])
    def get_films_by_specific_year(self, title="", year=None, limit=10, page=1):
        """
        Поиск фильмов по названию и конкретному году выпуска.

        :param title: Начало названия фильма (пустая строка = все фильмы)
        :param year: Конкретный год выпуска
        :param limit: Количество результатов на странице (1-100)
        :param page: Номер страницы (начиная с 1)
        :return: Список словарей с данными фильмов
        """
        pattern, limit, offset = self._default_validator(title, page, limit)
        films = self.mysql_db.select(FILMS_SPECIFIC_YEAR, (pattern, year, limit, offset))

        if self.mongo_db:
            self.mongo_db.log({
                "query_type" : "search_by_title_specific_year",
                "parameters" : {
                    "title": title,
                    "year": year,
                    "page": page,
                    "limit": limit
                },
                "result_count": len(films),
                "timestamp": datetime.now().isoformat()
            })

        return films


    @db_error_handler(default_return=[])
    def get_films_by_category(self, title="", min_year=0, max_year=9999, category=None, limit=10, page=1):
        """
        Поиск фильмов по категории, названию и диапазону лет.

        :param title: Начало названия фильма (пустая строка = все фильмы)
        :param min_year: Минимальный год выпуска
        :param max_year: Максимальный год выпуска
        :param category: Название категории для фильтрации
        :param limit: Количество результатов на странице (1-100)
        :param page: Номер страницы (начиная с 1)
        :return: Список словарей с данными фильмов
        """
        pattern, limit, offset = self._default_validator(title, page, limit)
        films = self.mysql_db.select(FILMS_BY_CATEGORY, (pattern, min_year, max_year, category, limit, offset))

        if self.mongo_db:
            self.mongo_db.log({
                "query_type" : "search_by_category",
                "parameters" : {
                    "title": title,
                    "min_year": min_year,
                    "max_year": max_year,
                    "category": category,
                    "page": page,
                    "limit": limit
                },
                "result_count": len(films),
                "timestamp": datetime.now().isoformat()
            })

        return films


    @db_error_handler(default_return=[])
    def get_films_by_actor(self):
        """Поиск фильмов по актёру (в разработке)."""
        pass


    def _default_validator(self, title, page, limit):
        if page < 1:
            page = 1
        if limit < 1:
            limit = 1
        if limit > 100:
            limit = 100

        offset = (page - 1) * limit
        pattern = f"{self._escape_like(title)}%" if title else "%"
        return pattern, limit, offset


    def _escape_like(self, s):
        return s.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
