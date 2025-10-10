from enum import Enum
from typing import List


class GenreOfFilmEnum(Enum):
    ACTION = 'Action'
    ADVENTURE = 'Adventure'
    ANIMATION = 'Animation'
    Biography = 'Biography'
    COMEDY = 'Comedy'
    CRIME = 'Crime'
    DOCUMENTARY = 'Documentary'
    DRAMA = 'Drama'
    FAMILY = 'Family'
    FANTASY = 'Fantasy'
    HISTORY = 'History'
    HORROR = 'Horror'
    MUSIC = 'Music'
    MUSICAL = 'Musical'
    MYSTERY = 'Mystery'
    ROMANCE = 'Romance'
    SPORT = 'Sport'
    THRILLER = 'Thriller'
    WAR = 'War'
    WESTERN = 'Western'
    NEWS = 'News'
    SHORT = 'Short'
    SCIFI = 'Sci-Fi'
    GAMESHOW = 'Game-Show'
    REALITYTV = 'Reality-TV'
    TALKSHOW = 'Talk-Show'

    @classmethod
    def safe_parse_list(cls, genre_string: str, split_literal: str = ',') -> List['GenreOfFilmEnum']:
        genres = []
        for genre_str in genre_string.split(split_literal):
            genre_clean = genre_str.strip()
            try:
                genres.append(cls(genre_clean))
            except ValueError:
                continue
        return genres
