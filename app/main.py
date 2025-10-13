import asyncio
import sys

from conf import Config, Logger
from handlers.telegram_setup_bot import setup_bot
from help_functions.database_functions import check_connect_database
from help_functions.migration_functions import run_migrations


async def main():
    if not check_connect_database():
        sys.exit(1)

    if not run_migrations():
        sys.exit(1)

    application = setup_bot(Config.BOT_TOKEN)

    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )

        Logger.info("Bot is running")

        await asyncio.Event().wait()

    Logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
