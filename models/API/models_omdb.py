from pydantic import BaseModel, field_validator
from typing import Union, List

from models.logic.GenreOfFilmEnum import GenreOfFilmEnum


class RatingMap(BaseModel):
    Source: str
    Value: str


class ErrorAboutFilmResponse(BaseModel):
    Response: bool
    Error: str


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
            return [GenreOfFilmEnum.safe_parse_list(value)]
        return value


APIOMDBResponse = Union[ErrorAboutFilmResponse, InfoAboutFilmResponse]
