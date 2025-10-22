import uuid

from sqlalchemy.future import select
from sqlalchemy import and_
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.postgresql_database import get_async_db_session
from handlers.telegram.keyboards.movie_keyboard import get_movie_keyboard
from handlers.telegram.telegram_utils.state_utils import *
from models.database.models_database import Movie


async def handle_movies_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "movies_section":
        reset_user_state(context)
        await query.edit_message_text(
            "🎬 *Фильмы и сериалы*\n\nВыберите действие:",
            parse_mode="Markdown",
            reply_markup=get_movie_keyboard()
        )

    elif query.data == "movies_my_movies":
        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                ).order_by(Movie.created_at.desc())
            )
        movies = movies_result.scalars().all()

        if movies:
            movies_text = "*Фильмы:*\n\n"
            for i, movie in enumerate(movies, 1):
                if movie.manual_rating is not None:
                    rating_text = f"🌟 {movie.manual_rating}/10"
                elif movie.imdb_rating is not None:
                    rating_text = f"⭐ {movie.imdb_rating}/10"
                else:
                    rating_text = "⚪ ---"
                movie_title = movie.manual_title[:25] + "..." if len(movie.manual_title) > 30 else movie.manual_title
                watched_status = "✅" if movie.is_viewed else "⏳"

                movies_text += f"{i}. *{movie_title}* {rating_text} | {watched_status}\n"
        else:
            movies_text = "В плейлисте пока нет фильмов"

        keyboard = [
            [InlineKeyboardButton("🔙 Назад", callback_data="movies_section")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"📊 Всего фильмов: {len(movies)}\n"
            f"{movies_text}",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "movies_add_movie":
        set_user_state(context, {
            "waiting_movie_add_name": True,
            "original_message_id": query.message.message_id,
            "original_chat_id": query.message.chat_id
        })

        keyboard = [
            [InlineKeyboardButton("❌ Отмена", callback_data="movies_section")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "📝 *Добавление фильма*\n\n"
            "Введите название нового фильма:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "movies_rate_movie":
        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                ).order_by(Movie.created_at.desc())
            )
            movies = movies_result.scalars().all()

            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="movies_section")]]

            for movie in movies:
                movie_title = movie.manual_title[:25] + "..." if len(movie.manual_title) > 30 else movie.manual_title
                keyboard.append([
                    InlineKeyboardButton(
                        f"🎬 {movie_title}",
                        callback_data=f"movies_rate_movie_{movie.internal_id}"
                    )
                ])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                f"🎯 Выберите фильм для оценки:" if movies else "У вас пока нет фильмов",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )


    elif query.data.startswith("movies_rate_movie_"):
        movie_id = uuid.UUID(query.data.replace("movies_rate_movie_", ""))

        keyboard = []
        ratings_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        row1 = []
        row2 = []
        for i in range(1, 11):
            button = InlineKeyboardButton(
                f"{ratings_emojis[i - 1]} {i}",
                callback_data=f"movies_set_rating_{movie_id}_{i}"
            )
            if i <= 5:
                row1.append(button)
            else:
                row2.append(button)
        keyboard.append(row1)
        keyboard.append(row2)
        keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="movies_section")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "🌟 *Оценка фильма*\n\n"
            "Выберите оценку от 1 до 10:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data.startswith("movies_set_rating_"):
        data = query.data.replace("movies_set_rating_", "")
        movie_id = uuid.UUID(data.split("_")[0])
        rate_movie = int(data.split("_")[1])

        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.internal_id == movie_id,
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                ).order_by(Movie.created_at.desc())
            )
            movie = movies_result.scalar_one_or_none()
            if not movie:
                await query.edit_message_text("❌ Фильм не найден.")
                return

            movie.manual_rating = rate_movie
            await session.commit()

            await query.edit_message_text(
                f"🎯 Фильм {movie.manual_title} успешно оценён на 🌟{rate_movie}!",
                parse_mode="Markdown",
                reply_markup=get_movie_keyboard()
            )


    elif query.data == "movies_mark_watched":
        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                ).order_by(Movie.created_at.desc())
            )
            movies = movies_result.scalars().all()

            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="movies_section")]]

            for movie in movies:
                movie_title = movie.manual_title[:25] + "..." if len(movie.manual_title) > 30 else movie.manual_title
                keyboard.append([
                    InlineKeyboardButton(
                        f"🎬 {movie_title}",
                        callback_data=f"movies_mark_watched_{movie.internal_id}"
                    )
                ])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                f"🎯 Выберите фильм для отметки просмотренным:" if movies else "У вас пока нет фильмов",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )

    elif query.data.startswith("movies_mark_watched_"):
        movie_id = uuid.UUID(query.data.replace("movies_mark_watched_", ""))

        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.internal_id == movie_id,
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                ).order_by(Movie.created_at.desc())
            )
            movie = movies_result.scalar_one_or_none()
            if not movie:
                await query.edit_message_text("❌ Фильм не найден.")
                return

            movie.is_viewed = True
            await session.commit()

            await query.edit_message_text(
                f"🎯 Фильм {movie.manual_title} успешно отмечен просмотренным ✅",
                parse_mode="Markdown",
                reply_markup=get_movie_keyboard()
            )

    elif query.data == "movies_delete_movie":
        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                ).order_by(Movie.created_at.desc())
            )
            movies = movies_result.scalars().all()

            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="movies_section")]]

            for movie in movies:
                movie_title = movie.manual_title[:25] + "..." if len(movie.manual_title) > 30 else movie.manual_title
                keyboard.append([
                    InlineKeyboardButton(
                        f"🎬 {movie_title}",
                        callback_data=f"movies_delete_movie_{movie.internal_id}"
                    )
                ])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                f"🎯 Выберите фильм для удаления:" if movies else "У вас пока нет фильмов",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )

    elif query.data.startswith("movies_delete_movie_"):
        movie_id = uuid.UUID(query.data.replace("movies_delete_movie_", ""))

        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.internal_id == movie_id,
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                ).order_by(Movie.created_at.desc())
            )
            movie = movies_result.scalar_one_or_none()
            if not movie:
                await query.edit_message_text("❌ Фильм не найден.")
                return

            movie.is_deleted = True
            await session.commit()

            await query.edit_message_text(
                f"🎯 Фильм {movie.manual_title} был успешно удалён 🗑️",
                parse_mode="Markdown",
                reply_markup=get_movie_keyboard()
            )
