import logging
import sys


def setup_logger() -> logging.Logger:
    logger = logging.getLogger('movie_and_series_watchlist_bot')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # file_handler = logging.FileHandler('app.log')
        # file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        # logger.addHandler(file_handler)

        logger.propagate = False

    return logger
