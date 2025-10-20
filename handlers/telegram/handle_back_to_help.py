from telegram import Update
from telegram.ext import ContextTypes

from handlers.telegram.handle_info import handle_info


async def handle_back_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await handle_info(update, context)
