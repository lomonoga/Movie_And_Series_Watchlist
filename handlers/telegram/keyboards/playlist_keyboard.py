from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_playlist_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Создать плейлист", callback_data="playlists_create_playlist")],
    [InlineKeyboardButton("📂 Мои плейлисты", callback_data="playlists_view_playlists")],
    [InlineKeyboardButton("🎬 Добавить в плейлист", callback_data="playlists_add_to_playlist")],
    [InlineKeyboardButton("👀 Просмотреть плейлист", callback_data="playlists_view_playlist")],
    [InlineKeyboardButton("🔙 Назад", callback_data="back_to_info")]
])
