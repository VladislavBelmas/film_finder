from datetime import datetime
from db.mongo_client import MongoDB
from db.mysql_client import MySql
from db.queries import *
from film_logger import db_error_handler


class MovieRepository:
    def __init__(self, mysql_db: MySql, mongo_db: MongoDB):
        self.mysql_db = mysql_db
        self.mongo_db = mongo_db


    @db_error_handler(default_return=[])
    def get_categories(self):
        return self.mysql_db.select(CATEGORIES)


    @db_error_handler(default_return=(1900, 2026))
    def years_range(self):
        min_year = self.mysql_db.select(MIN_FILM_YEAR)[0]["min_year"]
        max_year = self.mysql_db.select(MAX_FILM_YEAR)[0]["max_year"]
        return min_year, max_year


    @db_error_handler(default_return=[])
    def get_films(self, title="", min_year=0, max_year=9999, limit=10, page=1):
        offset = (page - 1) * limit
        pattern = f"{title}%" if title else "%"

        films = self.mysql_db.select(FILMS, (pattern, min_year, max_year, limit, offset))

        if self.mongo_db:
            self.mongo_db.log({
                "query_type" : "search_by_title",
                "parameters" : {
                    "title": title,
                    "min_year": min_year,
                    "max_year": max_year,
                    "page": page
                },
                "result_count": len(films),
                "timestamp": datetime.now().isoformat()
            })

        return films


    @db_error_handler(default_return=[])
    def get_films_by_specific_year(self, title="", year=2015, limit=10, page=1):
        offset = (page - 1) * limit
        pattern = f"{title}%" if title else "%"

        films = self.mysql_db.select(FILMS_SPECIFIC_YEAR, (pattern, year, limit, offset))

        if self.mongo_db:
            self.mongo_db.log({
                "query_type" : "search_by_title_specific_year",
                "parameters" : {
                    "title": title,
                    "year": year,
                    "page": page
                },
                "result_count": len(films),
                "timestamp": datetime.now().isoformat()
            })

        return films


    @db_error_handler(default_return=[])
    def get_films_by_category(self):
        pass


        return


    @db_error_handler(default_return=[])
    def get_films_by_actor(self):
        pass


        return