from sqlalchemy import Column, String, DateTime, Boolean, BigInteger, UUID, Double, ARRAY
from sqlalchemy.sql import func
from postgresql_database import Base


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    is_bot = Column(Boolean, index=True, nullable=False)
    first_name = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.user_id}, is_bot={self.is_bot}, name={self.first_name})>"


class Movie(Base):
    __tablename__ = 'Movies'

    movie_id = Column(UUID, primary_key=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    release_year = Column(BigInteger, index=True, nullable=False)
    genres = Column(A, nullable=False)
    auto_rating = Column(Double, nullable=False)
    manual_rating = Column(Double, nullable=False)
    is_viewed = Column(Boolean, nullable=False)

    is_deleted = Column(Boolean, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
