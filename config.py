"""Конфигурация подключений к базам данных MySQL и MongoDB."""

import os
from typing import Any
from dotenv import load_dotenv
import pymysql


load_dotenv()

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_NAME"),
    'cursorclass': pymysql.cursors.DictCursor
}


MONGO_CONFIG = {
    "uri": os.getenv("MONGO_URI"),
    "database": os.getenv("MONGO_DB"),
    "collection": os.getenv("MONGO_COLLECTION")
}
