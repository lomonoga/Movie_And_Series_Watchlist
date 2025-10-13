import sys

from telegram.ext import Application, Updater

from conf import Config
from help_functions.database_functions import check_connect_database
from help_functions.migration_functions import run_migrations


def main():
    if not check_connect_database():
        sys.exit(1)
    if not run_migrations():
        sys.exit(1)

    application = Application.builder().token(Config.BOT_TOKEN).build()


if __name__ == "__main__":
    main()
