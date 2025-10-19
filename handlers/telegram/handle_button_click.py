from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "section_movies":
        keyboard = [
            [InlineKeyboardButton("📝 Добавить фильм", callback_data="add_movie")],
            [InlineKeyboardButton("🎞️ Мои фильмы", callback_data="my_movies")],
            [InlineKeyboardButton("⭐ Оценить фильм", callback_data="rate_movie")],
            [InlineKeyboardButton("✅ Отметить просмотренным", callback_data="mark_watched")],
            [InlineKeyboardButton("🗑️ Удалить фильм", callback_data="delete_movie")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "🎬 *Фильмы и сериалы*\n\nВыберите действие:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "section_playlists":
        keyboard = [
            [InlineKeyboardButton("➕ Создать плейлист", callback_data="create_playlist")],
            [InlineKeyboardButton("📂 Мои плейлисты", callback_data="view_playlists")],
            [InlineKeyboardButton("🎬 Добавить в плейлист", callback_data="add_to_playlist")],
            [InlineKeyboardButton("👀 Просмотреть плейлист", callback_data="view_playlist")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "📁 *Плейлисты*\n\nВыберите действие:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "section_recommendations":
        keyboard = [
            [InlineKeyboardButton("🎲 Получить рекомендацию", callback_data="get_recommendation")],
            [InlineKeyboardButton("📊 Статистика просмотров", callback_data="view_stats")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "🎯 *Рекомендации*\n\nПолучите персональные рекомендации:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "back_to_main":
        keyboard = [
            [InlineKeyboardButton("🎬 Фильмы и сериалы", callback_data="movie_keyboard")],
            [InlineKeyboardButton("📁 Плейлисты", callback_data="playlist_keyboard")],
            [InlineKeyboardButton("🎯 Рекомендации", callback_data="recommendation_keyboard")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "🎬 *Главное меню*\n\nВыберите раздел:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )