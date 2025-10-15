from sqlalchemy import Column, String, DateTime, Boolean, BigInteger, UUID, ARRAY, Enum, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.postgresql_database import Base
from models.logic.GenreOfFilmEnum import GenreOfFilmEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    is_bot = Column(Boolean, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)

    count_views_movies = Column(BigInteger, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    playlists = relationship('Playlist', back_populates='user', order_by='Playlist.updated_at')
    movies = relationship('Movie', back_populates='user', order_by='Movie.imdb_rating')


class Movie(Base):
    __tablename__ = 'movies'

    internal_id = Column(UUID, primary_key=True, index=True, nullable=False)
    manual_title = Column(String(255), nullable=False)
    manual_rating = Column(Float, nullable=False)

    omdb_genres = Column(ARRAY(Enum(GenreOfFilmEnum)), nullable=False)
    imdb_rating = Column(Float, nullable=False)

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    playlist_id = Column(UUID, ForeignKey('playlists.id'), nullable=True)

    is_viewed = Column(Boolean, nullable=False, default=False)

    is_deleted = Column(Boolean, index=True, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship('User', back_populates='movies')
    playlist = relationship('Playlist', back_populates='movies')


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(UUID, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    is_deleted = Column(Boolean, index=True, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship('User', back_populates='playlists')
    movies = relationship('Movie', back_populates='playlist', order_by='Movie.imdb_rating')
