from pydantic import BaseModel, field_validator
from typing import List

from models.logic.GenreOfFilmEnum import GenreOfFilmEnum


class ErrorAboutFilmResponse(BaseModel):
    Response: bool
    Error: str


class RatingMap(BaseModel):
    Source: str
    Value: str


class InfoAboutFilmResponse(BaseModel):
    Title: str
    Year: int
    Rated: str
    Released: str
    Runtime: str
    Genre: List[GenreOfFilmEnum]
    Director: str
    Writer: str
    Actors: str
    Plot: str
    Language: str
    Country: str
    Awards: str
    Poster: str
    Ratings: List[RatingMap]
    Metascore: str
    imdbRating: float
    imdbVotes: str
    imdbID: str
    Type: str
    DVD: str
    BoxOffice: str
    Production: str
    Website: str
    Response: bool

    @field_validator('Genre', mode='before')
    @classmethod
    def parse_genres(cls, value):
        if isinstance(value, str):
            return GenreOfFilmEnum.safe_parse_list(value)
        return value


def parse_omdb_response(data: dict) -> ErrorAboutFilmResponse | InfoAboutFilmResponse:
    if data.get('Response') == 'False':
        return ErrorAboutFilmResponse(**data)
    else:
        return InfoAboutFilmResponse(**data)
