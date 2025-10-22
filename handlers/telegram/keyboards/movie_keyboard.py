from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_movie_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Создать плейлист", callback_data="playlists_create_playlist")],
        [InlineKeyboardButton("📂 Мои плейлисты", callback_data="playlists_view_playlists")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_info")]
    ])
