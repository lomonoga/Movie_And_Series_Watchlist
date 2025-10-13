__version__ = "1.0.0"
__author__ = "lomonoga"

from .config import Config
from .logger import setup_logger

Config = Config()
Logger = setup_logger()

__all__ = ['Config', 'Logger']
