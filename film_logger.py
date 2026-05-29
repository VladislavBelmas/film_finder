import logging
import functools

logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)


logger = logging.getLogger(__name__)


def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} работает штатно")
            return result

        except Exception as e:
            logger.error(f"Ошибка в {func.__name__}: {e}")

    return wrapper()