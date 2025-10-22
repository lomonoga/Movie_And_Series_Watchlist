from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_movie_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎞️ Мои фильмы", callback_data="movies_my_movies")],
        [InlineKeyboardButton("📝 Добавить фильм", callback_data="movies_add_movie")],
        [InlineKeyboardButton("⭐ Оценить фильм", callback_data="movies_rate_movie")],
        [InlineKeyboardButton("✅ Отметить просмотренным", callback_data="movies_mark_watched")],
        [InlineKeyboardButton("🗑️ Удалить фильм", callback_data="movies_delete_movie")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_info")]
    ])
