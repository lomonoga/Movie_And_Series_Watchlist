from telegram import Update
from telegram.ext import ContextTypes

from handlers.telegram.help_handler import help_command


async def handle_back_to_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await help_command(update, context)
