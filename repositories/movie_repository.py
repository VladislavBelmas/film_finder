from datetime import datetime
from typing import Optional
from db.mongo_client import MongoDB
from db.mysql_client import MySql
from db.queries import (
    CATEGORIES,
    MIN_FILM_YEAR,
    MAX_FILM_YEAR,
    FILMS,
    FILMS_SPECIFIC_YEAR,
    FILMS_BY_CATEGORY
)
from film_logger import db_error_handler


class MovieRepository:
    """Репозиторий для работы с данными фильмов из MySQL и логирования в MongoDB."""

    def __init__(self, mysql_db: MySql, mongo_db: Optional[MongoDB]) -> None:
        self.mysql_db = mysql_db
        self.mongo_db = mongo_db

    @db_error_handler(default_return=[])
    def get_categories(self) -> list[dict[str, any]]:
        """Возвращает список всех категорий фильмов."""
        return self.mysql_db.select(CATEGORIES)

    @db_error_handler(default_return=(1900, 2026))
    def years_range(self) -> tuple[int, int]:
        """Возвращает диапазон годов выпуска фильмов в базе (min_year, max_year)."""
        min_year = self.mysql_db.select(MIN_FILM_YEAR)[0]["min_year"]
        max_year = self.mysql_db.select(MAX_FILM_YEAR)[0]["max_year"]
        return min_year, max_year

    @db_error_handler(default_return=[])
    def get_films(self, title: str = "", min_year: int = 0, max_year: int = 9999,
                  limit: int = 10, page: int = 1) -> list[dict[str, any]]:
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
                "query_type": "search_by_title",
                "parameters": {
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
    def get_films_by_specific_year(self, title: str = "", year: Optional[int] = None,
                                    limit: int = 10, page: int = 1) -> list[dict[str, any]]:
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
                "query_type": "search_by_title_specific_year",
                "parameters": {
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
    def get_films_by_category(self, title: str = "", min_year: int = 0, max_year: int = 9999,
                               category: Optional[str] = None, limit: int = 10, page: int = 1) -> list[dict[str, any]]:
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
                "query_type": "search_by_category",
                "parameters": {
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
    def get_films_by_actor(self) -> list[dict[str, any]]:
        """Поиск фильмов по актёру (в разработке)."""
        return []

    def get_statistics(self) -> Optional[dict[str, any]]:
        """Возвращает статистику из MongoDB."""
        if not self.mongo_db:
            return None
        return self.mongo_db.get_statistics()

    def _default_validator(self, title: str, page: int, limit: int) -> tuple[str, int, int]:
        """Валидирует и нормализует параметры запроса."""
        if page < 1:
            page = 1
        if limit < 1:
            limit = 1
        if limit > 100:
            limit = 100

        offset = (page - 1) * limit
        pattern = f"{self._escape_like(title)}%" if title else "%"
        return pattern, limit, offset

    def _escape_like(self, s: str) -> str:
        """Экранирует специальные символы для SQL LIKE."""
        return s.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
