from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def handle_movies_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "movies_section":
        keyboard = [
            [InlineKeyboardButton("📝 Добавить фильм", callback_data="add_movie")],
            [InlineKeyboardButton("🎞️ Мои фильмы", callback_data="my_movies")],
            [InlineKeyboardButton("⭐ Оценить фильм", callback_data="rate_movie")],
            [InlineKeyboardButton("✅ Отметить просмотренным", callback_data="mark_watched")],
            [InlineKeyboardButton("🗑️ Удалить фильм", callback_data="delete_movie")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "🎬 *Фильмы и сериалы*\n\nВыберите действие:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )