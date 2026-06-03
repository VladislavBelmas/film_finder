"""Точка входа приложения Film Finder."""

from config import MYSQL_CONFIG, MONGO_CONFIG
from db.mongo_client import MongoDB
from db.mysql_client import MySql
from repositories.movie_repository import MovieRepository
from ui import Menu


def main():
    """Запускает приложение для поиска фильмов."""
    with MySql(MYSQL_CONFIG) as mysql, MongoDB(MONGO_CONFIG) as mongo:
        repo = MovieRepository(mysql, mongo)
        menu = Menu(repo)
        menu.run()


if __name__ == "__main__":
    main()