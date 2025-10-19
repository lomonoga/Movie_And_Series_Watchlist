from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Фильмы и сериалы", callback_data="section_movies")],
        [InlineKeyboardButton("📁 Плейлисты", callback_data="section_playlists")],
        [InlineKeyboardButton("🎯 Рекомендации", callback_data="section_recommendations")],
    ])
