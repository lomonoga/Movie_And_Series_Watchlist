from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from conf import Logger
from handlers.telegram.handle_back_to_help import handle_back_to_help
from handlers.telegram.handle_movies_block import handle_movies_block
from handlers.telegram.handle_playlists_block import handle_playlists_block
from handlers.telegram.handle_recommendations_block import handle_recommendations_block
from handlers.telegram.help_handler import help_command
from handlers.telegram.start_handler import start_command


def setup_bot(token: str) -> Application:
    application = Application.builder().token(token).build()
    application.add_error_handler(_error_handler)

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CallbackQueryHandler(handle_movies_block, pattern="^movies_"))
    application.add_handler(CallbackQueryHandler(handle_playlists_block, pattern="^playlists_"))
    application.add_handler(CallbackQueryHandler(handle_recommendations_block, pattern="^recommendations_"))
    application.add_handler(CallbackQueryHandler(handle_back_to_help, pattern="back_to_help"))

    return application


async def _error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Logger.error(f"Error: {context.error}")
