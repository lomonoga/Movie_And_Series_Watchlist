from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def handle_recommendations_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "recommendations_section":
        keyboard = [
            [InlineKeyboardButton("🎲 Получить рекомендацию", callback_data="get_recommendation")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "🎯 *Рекомендации*\n\nПолучите персональные рекомендации:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
