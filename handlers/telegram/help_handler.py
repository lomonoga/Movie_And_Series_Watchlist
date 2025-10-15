from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 Доступные разделы:

🎬 Фильмы и сериалы
• Добавить фильм или сериал
• Просмотреть мои фильмы и сериалы
• Оценить фильм или сериал
• Отметить фильм или сериал просмотренным
• Удалить фильм или сериал

📂 Плейлисты
• Создать плейлист
• Просмотреть плейлисты
• Добавить фильм или сериал в плейлист
• Просмотреть список фильмов и сериалов в плейлисте  

🎯 Рекомендации:
• Получить рекомендацию по просмотру фильма из вашего списка
    """

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎬 Фильмы и сериалы", callback_data="section_movies")
        ],
        [
            InlineKeyboardButton("📁 Плейлисты", callback_data="section_playlists")
        ],
        [
            InlineKeyboardButton("🎯 Рекомендации", callback_data="section_recommendations"),
        ]
    ])

    await update.message.reply_text(
        help_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
