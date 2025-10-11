from sqlalchemy import Column, String, DateTime, Boolean, BigInteger, UUID, ARRAY, Enum, Float
from sqlalchemy.sql import func

from database.postgresql_database import Base
from models.logic.GenreOfFilmEnum import GenreOfFilmEnum


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    is_bot = Column(Boolean, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)

    count_views_movies = Column(BigInteger, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.user_id}, is_bot={self.is_bot}, name={self.first_name})>"


class Movie(Base):
    __tablename__ = 'Movies'

    internal_movie_id = Column(UUID, primary_key=True, index=True, nullable=False)
    manual_title = Column(String(255), nullable=False)
    manual_rating = Column(Float, nullable=False)

    omdb_genres = Column(ARRAY(Enum(GenreOfFilmEnum)), nullable=False)
    imdb_rating = Column(Float, nullable=False)

    is_viewed = Column(Boolean, nullable=False, default=False)

    is_deleted = Column(Boolean, index=True, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
