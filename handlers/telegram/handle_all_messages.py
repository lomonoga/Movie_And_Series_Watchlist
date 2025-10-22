import uuid

from sqlalchemy.future import select
from sqlalchemy import and_
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from conf import Logger
from database.postgresql_database import get_async_db_session
from handlers.telegram.keyboards.movie_keyboard import get_movie_keyboard
from handlers.telegram.keyboards.playlist_keyboard import get_playlist_keyboard
from handlers.telegram.telegram_utils.state_utils import *
from models.database.models_database import Movie, Playlist
from models.foreign_api.models_omdb import parse_omdb_response, InfoAboutFilmResponse
from models.logic.GenreOfFilmEnum import GenreOfFilmEnum
from services.omdb_api_service import get_movie_details


async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_user_waiting_input(context):
        return

    if context.user_data.get("waiting_movie_add_name"):
        if "original_chat_id" not in context.user_data or "original_message_id" not in context.user_data:
            reset_user_state(context)
            await update.message.reply_text(
                "❌ Произошла ошибка. Возврат в меню.",
                reply_markup=get_movie_keyboard()
            )
            return

        movie_name = update.message.text

        await update.message.delete()

        async with get_async_db_session() as session:
            result = await session.execute(select(Movie).where(
                and_(
                    Movie.manual_title == movie_name,
                    Movie.user_id == update.effective_user.id,
                    Movie.is_deleted == False
                )
            ))
            movie = result.scalar_one_or_none()

            if not movie:
                result_of_film_api = parse_omdb_response(await get_movie_details(name_of_movie=movie_name))
                omdb_genres: List[GenreOfFilmEnum] | None = None
                imdb_rating: float | None = None
                match result_of_film_api:
                    case InfoAboutFilmResponse() as film_info:
                        omdb_genres = film_info.Genre
                        imdb_rating = film_info.imdbRating
                    case _:
                        pass

                movie_db = Movie(
                    internal_id=uuid.uuid4(),
                    manual_title=movie_name,
                    omdb_genres=omdb_genres,
                    imdb_rating=imdb_rating,
                    user_id=update.effective_user.id
                )
                session.add(movie_db)
                await session.commit()

                context.user_data["waiting_movie_add_name"] = False

                Logger.info(f"New movie added with name: {movie_name} for user: {update.effective_user.id}")

                await context.bot.edit_message_text(
                    chat_id=context.user_data["original_chat_id"],
                    message_id=context.user_data["original_message_id"],
                    text=f"✅ Фильм '*{movie_name}*' успешно добавлен!\n\n"
                         "Выберите действие:",
                    parse_mode="Markdown",
                    reply_markup=get_movie_keyboard()
                )

                context.user_data.pop("original_message_id", None)
                context.user_data.pop("original_chat_id", None)

            else:
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("❌ Отмена", callback_data="movies_section")]
                ])

                await context.bot.edit_message_text(
                    chat_id=context.user_data["original_chat_id"],
                    message_id=context.user_data["original_message_id"],
                    text=f"❌ Фильм '*{movie_name}*' уже существует!\n\n"
                         "Введите другое название фильма:",
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )

                context.user_data["waiting_movie_add_name"] = True

    elif context.user_data.get("waiting_playlist_create_name"):
        if "original_chat_id" not in context.user_data or "original_message_id" not in context.user_data:
            reset_user_state(context)
            await update.message.reply_text(
                "❌ Произошла ошибка. Возврат в меню.",
                reply_markup=get_playlist_keyboard()
            )
            return

        playlist_name = update.message.text

        await update.message.delete()

        async with get_async_db_session() as session:
            result = await session.execute(select(Playlist).where(
                and_(
                    Playlist.name == playlist_name,
                    Playlist.user_id == update.effective_user.id,
                    Playlist.is_deleted == False
                )
            ))
            playlist = result.scalar_one_or_none()

            if not playlist:
                playlist_db = Playlist(
                    id=uuid.uuid4(),
                    name=playlist_name,
                    user_id=update.effective_user.id
                )
                session.add(playlist_db)
                await session.commit()

                context.user_data["waiting_playlist_create_name"] = False

                Logger.info(f"New playlist created with name: {playlist_name} for user: {update.effective_user.id}")

                await context.bot.edit_message_text(
                    chat_id=context.user_data["original_chat_id"],
                    message_id=context.user_data["original_message_id"],
                    text=f"✅ Плейлист '*{playlist_name}*' успешно создан!\n\n"
                         "📁 *Плейлисты*\n\nВыберите действие:",
                    parse_mode="Markdown",
                    reply_markup=get_playlist_keyboard()
                )

                context.user_data.pop("original_message_id", None)
                context.user_data.pop("original_chat_id", None)

            else:
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("❌ Отмена", callback_data="playlists_section")]
                ])

                await context.bot.edit_message_text(
                    chat_id=context.user_data["original_chat_id"],
                    message_id=context.user_data["original_message_id"],
                    text=f"❌ Плейлист '*{playlist_name}*' уже существует!\n\n"
                         "Введите другое название для нового плейлиста:",
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )

                context.user_data["waiting_playlist_create_name"] = True
