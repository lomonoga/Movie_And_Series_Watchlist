from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def handle_playlists_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "playlists_section":
        keyboard = [
            [InlineKeyboardButton("➕ Создать плейлист", callback_data="playlists_create_playlist")],
            [InlineKeyboardButton("📂 Мои плейлисты", callback_data="playlists_view_playlists")],
            [InlineKeyboardButton("🎬 Добавить в плейлист", callback_data="playlists_add_to_playlist")],
            [InlineKeyboardButton("👀 Просмотреть плейлист", callback_data="playlists_view_playlist")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "📁 *Плейлисты*\n\nВыберите действие:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

