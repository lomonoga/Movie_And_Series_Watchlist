from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from conf import Logger
from handlers.telegram.handle_button_click import handle_button_click
from handlers.telegram.help_handler import help_command
from handlers.telegram.start_handler import start_command


def setup_bot(token: str) -> Application:
    application = Application.builder().token(token).build()
    application.add_error_handler(_error_handler)

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CallbackQueryHandler(handle_button_click))

    return application


async def _error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Logger.error(f"Error: {context.error}")
