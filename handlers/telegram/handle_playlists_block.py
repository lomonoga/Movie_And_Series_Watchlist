from sqlalchemy.future import select
from sqlalchemy import and_
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from conf import Logger
from database.postgresql_database import get_async_db_session
from handlers.telegram.keyboards.playlist_keyboard import get_playlist_keyboard
from handlers.telegram.telegram_utils.state_utils import *
from models.database.models_database import Playlist


async def handle_playlists_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "playlists_section":
        reset_user_state(context)

        await query.edit_message_text(
            "📁 *Плейлисты*\n\nВыберите действие:",
            parse_mode="Markdown",
            reply_markup=get_playlist_keyboard()
        )

    elif query.data == "playlists_create_playlist":
        set_user_state(context, {
            "waiting_create_playlist_name": True,
            "original_message_id": query.message.message_id,
            "original_chat_id": query.message.chat_id
        })

        keyboard = [
            [InlineKeyboardButton("❌ Отмена", callback_data="playlists_section")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "📝 *Создание плейлиста*\n\n"
            "Введите название для нового плейлиста:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "playlists_view_playlists":
        async with get_async_db_session() as session:
            result = await session.execute(
                select(Playlist).where(
                    and_(
                        Playlist.user_id == update.effective_user.id,
                        Playlist.is_deleted == False
                    )
                ).order_by(Playlist.created_at.desc())
            )
            playlists = result.scalars().all()

            keyboard = []
            for playlist in playlists:
                keyboard.append([
                    InlineKeyboardButton(
                        f"🎬 {playlist.name}",
                        callback_data=f"playlist_show_{playlist.id}"
                    )
                ])

            keyboard.extend([
                [InlineKeyboardButton("🔙 Назад", callback_data="playlists_section")]
            ])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                f"📂 *Мои плейлисты*\n\n",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )

    # elif query.data == "playlists_add_to_playlist":
    #
    # elif query.data == "playlists_view_playlist":
