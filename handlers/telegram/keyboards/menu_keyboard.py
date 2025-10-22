from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Фильмы", callback_data="movies_section")],
        [InlineKeyboardButton("📁 Плейлисты", callback_data="playlists_section")],
        [InlineKeyboardButton("🎯 Рекомендации", callback_data="recommendations_section")],
    ])
