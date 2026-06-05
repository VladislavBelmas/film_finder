"""Точка входа приложения Film Finder."""

from typing import Optional
from config import MYSQL_CONFIG, MONGO_CONFIG
from db.mongo_client import MongoDB
from db.mysql_client import MySql
from repositories.movie_repository import MovieRepository
from ui import Menu


def main() -> None:
    """Запускает приложение для поиска фильмов."""
    with MySql(MYSQL_CONFIG) as mysql:
        try:
            mongo = MongoDB(MONGO_CONFIG).__enter__()
        except Exception:
            mongo = None
            print("MongoDB недоступен, логирование отключено")

        repo = MovieRepository(mysql, mongo)
        menu = Menu(repo)
        menu.run()

        if mongo:
            try:
                mongo.__exit__(None, None, None)
            except Exception:
                pass


if __name__ == "__main__":
    main()
