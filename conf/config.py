import logging
import os
from typing import ClassVar, get_type_hints
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self._setup()

    _BOT_TOKEN_ENV: ClassVar[str] = 'Movie_And_Series_Watchlist_TELEGRAM_BOT_TOKEN'
    _DATABASE_URL_ENV: ClassVar[str] = 'Movie_And_Series_Watchlist_DATABASE_URL'
    _DATABASE_USER: ClassVar[str] = 'Movie_And_Series_Watchlist_DATABASE_USER'
    _DATABASE_PASSWORD: ClassVar[str] = 'Movie_And_Series_Watchlist_DATABASE_PASSWORD'
    _MOVIE_API_KEY: ClassVar[str] = 'Movie_And_Series_Watchlist_OMDB_API_KEY'

    BOT_TOKEN: ClassVar[str]
    DATABASE_URL: ClassVar[str]
    DATABASE_USER: ClassVar[str]
    DATABASE_PASSWORD: ClassVar[str]
    MOVIE_API_KEY: ClassVar[str]

    @classmethod
    def _get_required_fields(cls) -> list[str]:
        required = []
        annotations = get_type_hints(cls, include_extras=True)
        for name, annotation in annotations.items():
            if not name.isupper():
                continue
            if hasattr(annotation, '__origin__') and annotation.__origin__ is ClassVar:
                if not hasattr(cls, name):
                    required.append(name)
        return required

    @classmethod
    def _get_env(cls, name: str, required: bool = True) -> str | None:
        value = os.getenv(name)
        if not value and required:
            logging.error(f'Environment variable "{name}" not found!')
            logging.info(f'Set the environment variable: {name}.')
            raise ValueError(f'Required environment variable "{name}" is not set.')
        return value

    @classmethod
    def _load(cls):
        load_dotenv()

        cls.BOT_TOKEN = cls._get_env(cls._BOT_TOKEN_ENV)
        cls.DATABASE_URL = cls._get_env(cls._DATABASE_URL_ENV)
        cls.DATABASE_USER = cls._get_env(cls._DATABASE_USER)
        cls.DATABASE_PASSWORD = cls._get_env(cls._DATABASE_PASSWORD)
        cls.MOVIE_API_KEY = cls._get_env(cls._MOVIE_API_KEY)

    @classmethod
    def _validate(cls) -> None:
        required_fields = cls._get_required_fields()
        for field in required_fields:
            if not getattr(cls, field, None):
                raise ValueError(f'Field {field} is not set. Call Config.load() before using.')
        logging.info('✅ The configuration has been successfully loaded and validated.')

    @classmethod
    def _setup(cls) -> None:
        cls._load()
        cls._validate()
