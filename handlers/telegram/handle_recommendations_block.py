import random

from sqlalchemy.future import select
from sqlalchemy import and_
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.postgresql_database import get_async_db_session
from models.database.models_database import Movie
from models.logic.GenreOfFilmEnum import GenreOfFilmEnum


async def handle_recommendations_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "recommendations_section":
        keyboard = [
            [InlineKeyboardButton(text="🎲 Получить рекомендацию по фильму",
                                  callback_data="recommendations_get_recommendation")],
            [InlineKeyboardButton(text="🎲 Получить рекомендацию по выбранным жанрам",
                                  callback_data="recommendations_get_recommendation_by_genres")],
            [InlineKeyboardButton(text="🔙 Назад",
                                  callback_data="back_to_info")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "🎯 *Рекомендации*\n\nПолучите персональные рекомендации:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "recommendations_get_recommendation":
        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.user_id == update.effective_user.id,
                        Movie.is_viewed == False,
                        Movie.is_deleted == False
                    )
                )
            )
            movies = movies_result.scalars().all()

        weights = []
        for movie in movies:
            if movie.manual_rating is not None:
                rating = movie.manual_rating
            elif movie.imdb_rating is not None:
                rating = movie.imdb_rating
            else:
                rating = None

            if rating is not None:
                weight = rating ** 1.1
            else:
                weight = random.uniform(0.1, 5.0)

            weights.append(weight)

        if movies:
            recommended_movie = random.choices(movies, weights=weights, k=1)[0]
            if recommended_movie.manual_rating is not None:
                rating_text = f"🌟 {recommended_movie.manual_rating}/10"
            elif recommended_movie.imdb_rating is not None:
                rating_text = f"⭐ {recommended_movie.imdb_rating}/10"
            else:
                rating_text = "⚪ ---"
            movie_text = f"Предлагаем посмотреть:\n\n{recommended_movie.manual_title}\n\n {rating_text}"
        else:
            movie_text = "У вас пока нет фильмов"

        keyboard = [
            [InlineKeyboardButton("🔙 Назад", callback_data="recommendations_section")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"{movie_text}",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "recommendations_get_recommendation_by_genres":
        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.user_id == update.effective_user.id,
                        Movie.is_viewed == False,
                        Movie.is_deleted == False
                    )
                )
            )
            movies = movies_result.scalars().all()

        all_genres = set[GenreOfFilmEnum]()
        for movie in movies:
            if movie.omdb_genres:
                all_genres.update(movie.omdb_genres)

        keyboard = [
            [InlineKeyboardButton("🔙 Назад", callback_data="recommendations_section")]
        ]

        genres_list = sorted(list(all_genres), key=lambda x: x.value)
        for i in range(0, len(genres_list), 3):
            row = []
            for genre in genres_list[i:i + 3]:
                row.append(InlineKeyboardButton(
                    genre.value,
                    callback_data=f"recommendations_get_by_genre_{genre.value}"
                ))
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🎭 *Фильтр по жанрам*\n\n"
            f"📊 Всего жанров: {len(all_genres)}\n"
            f"🎬 Всего фильмов: {len(movies)}\n\n"
            f"Выберите жанр:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data.startswith("recommendations_get_by_genre_"):
        genre_enum = GenreOfFilmEnum(query.data.replace("recommendations_get_by_genre_", ""))

        async with get_async_db_session() as session:
            movies_result = await session.execute(
                select(Movie).where(
                    and_(
                        Movie.omdb_genres.any(genre_enum),
                        Movie.user_id == update.effective_user.id,
                        Movie.is_deleted == False
                    )
                )
            )
            movies = movies_result.scalars().all()

        weights = []
        for movie in movies:
            if movie.manual_rating is not None:
                rating = movie.manual_rating
            elif movie.imdb_rating is not None:
                rating = movie.imdb_rating
            else:
                rating = None

            if rating is not None:
                weight = rating ** 1.1
            else:
                weight = random.uniform(0.1, 5.0)

            weights.append(weight)

        if movies:
            recommended_movie = random.choices(movies, weights=weights, k=1)[0]
            if recommended_movie.manual_rating is not None:
                rating_text = f"🌟 {recommended_movie.manual_rating}/10"
            elif recommended_movie.imdb_rating is not None:
                rating_text = f"⭐ {recommended_movie.imdb_rating}/10"
            else:
                rating_text = "⚪ ---"
            movie_text = f"Предлагаем посмотреть:\n\n{recommended_movie.manual_title}\n\n {rating_text}"
        else:
            movie_text = "У вас пока нет фильмов"

        keyboard = [
            [InlineKeyboardButton("🔙 Назад", callback_data="recommendations_section")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"{movie_text}",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
