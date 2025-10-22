import uuid

from sqlalchemy.future import select
from sqlalchemy import and_
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from conf import Logger
from database.postgresql_database import get_async_db_session
from handlers.telegram.keyboards.playlist_keyboard import get_playlist_keyboard
from handlers.telegram.telegram_utils.state_utils import *
from models.database.models_database import Playlist, Movie


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
                        callback_data=f"playlists_show_{playlist.id}"
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

    elif query.data.startswith("playlists_show_"):
        playlist_id = uuid.UUID(query.data.replace("playlists_show_", ""))

        async with get_async_db_session() as session:
            result = await session.execute(
                select(Playlist).where(
                    and_(
                        Playlist.id == playlist_id,
                        Playlist.user_id == update.effective_user.id,
                        Playlist.is_deleted == False
                    )
                )
            )
            playlist = result.scalar_one_or_none()

            if not playlist:
                await query.edit_message_text("❌ Плейлист не найден.")
                return

            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.playlist_id == playlist_id,
                        Movie.is_deleted == False
                    )
                ).order_by(Movie.created_at.desc())
            )
            movies = movies_result.scalars().all()

            if movies:
                movies_text = "*Фильмы в плейлисте:*\n\n"
                for i, movie in enumerate(movies, 1):
                    if movie.manual_rating is not None:
                        rating_text = f"🌟 {movie.manual_rating}/10"
                    elif movie.imdb_rating is not None:
                        rating_text = f"⭐ {movie.imdb_rating}/10"
                    else:
                        rating_text = "⚪ ---"

                    watched_status = "✅" if movie.is_viewed else "⏳"
                    movies_text += f"{i}. *{movie.manual_title}* {rating_text} | {watched_status}\n"
            else:
                movies_text = "В плейлисте пока нет фильмов"

            keyboard = [
                [InlineKeyboardButton("🎬 Добавить фильм",
                                      callback_data=f"playlists_select_playlist_{playlist.id}")],
                [InlineKeyboardButton("📂 Все плейлисты", callback_data="playlists_view_playlists")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                f"🎬 *{playlist.name}*\n\n"
                f"📊 Фильмов: {len(movies)}\n"
                f"📅 Создан: {playlist.created_at.strftime('%d.%m.%Y')}\n\n"
                f"{movies_text}",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )

    elif query.data.startswith("playlists_select_playlist_"):
        playlist_id = uuid.UUID(query.data.replace("playlists_select_playlist_", ""))

        set_user_state(context, {
            "playlists_add_movie_playlist_id": playlist_id
        })

        async with get_async_db_session() as session:
            result = await session.execute(
                select(Playlist).where(
                    and_(
                        Playlist.id == playlist_id,
                        Playlist.user_id == update.effective_user.id,
                        Playlist.is_deleted == False
                    )
                )
            )
            playlist = result.scalar_one_or_none()

            if not playlist:
                await query.edit_message_text("❌ Плейлист не найден.")
                return

            all_movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.playlist_id.is_(None),
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                ).order_by(Movie.created_at.desc())
            )
            movies = all_movies_result.scalars().all()

        keyboard = []
        for movie in movies:
            movie_title = movie.manual_title[:25] + "..." if len(movie.manual_title) > 30 else movie.manual_title
            keyboard.append([
                InlineKeyboardButton(
                    f"🎬 {movie_title}",
                    callback_data=f"playlists_add_movie_{movie.internal_id}"
                )
            ])

        keyboard.append(
            [InlineKeyboardButton("🔙 Назад", callback_data="playlists_section")]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"📁 *{playlist.name}*\n\n🎯 Выберите фильм для добавления:" if movies else "У вас пока нет фильмов",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data.startswith("playlists_add_movie_"):
        movie_id = uuid.UUID(query.data.replace("playlists_add_movie_", ""))
        playlist_id = get_user_state(context, "playlists_add_movie_playlist_id")
        reset_user_state(context, list("playlists_add_movie_playlist_id"))

        async with get_async_db_session() as session:
            playlist_result = await session.execute(
                select(Playlist).where(
                    and_(
                        Playlist.id == playlist_id,
                        Playlist.user_id == update.effective_user.id,
                        Playlist.is_deleted == False
                    )
                )
            )
            playlist = playlist_result.scalar_one_or_none()

            movie_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.internal_id == movie_id,
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                )
            )
            movie = movie_result.scalar_one_or_none()

            if not playlist or not movie:
                await query.edit_message_text("❌ Плейлист или фильм не найден.")
                return

            movie.playlist_id = playlist_id
            await session.commit()
            Logger.info(f"Movie with id: {movie_id} added in playlist with id: {playlist_id}")

            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🎬 Добавить еще фильм",
                                         callback_data=f"playlists_select_playlist_{playlist_id}"),
                    InlineKeyboardButton("📂 К плейлистам",
                                         callback_data="playlists_section")
                ]
            ])

            await query.edit_message_text(
                f"✅ Фильм *{movie.manual_title}* успешно добавлен в плейлист *{playlist.name}*!",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
