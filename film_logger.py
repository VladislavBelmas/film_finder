import logging
import functools
import pymysql

logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


logger = logging.getLogger(__name__)


def logger_decorator(func):
    """Декоратор для логирования выполнения функций и их ошибок."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} работает штатно")
            return result
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper


def db_error_handler(default_return=None):
    """
    Декоратор для обработки ошибок базы данных.

    :param default_return: значение, возвращаемое при ошибке
    :return: декоратор
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except pymysql.Error:
                print("База данных временно недоступна")
                return default_return
        return wrapper
    return decorator