import asyncio
import aiohttp

from conf import Config
from models.API.models_omdb import APIOMDBResponse


async def get_movie_details(name_of_movie: str) -> dict:
    omdb_url = 'https://www.omdbapi.com/'
    params = {
        't': name_of_movie,
        'type': 'movie',
        'plot': 'short',
        'r': 'json',
        'v': '1',
        'apikey': Config.MOVIE_API_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(omdb_url, params=params) as response:
            if 200 >= response.status < 300:
                return await response.json()
            else:
                raise Exception(f"HTTP {response.status}")

async def main():
    val = await get_movie_details('Mom')
    return APIOMDBResponse(**val)

print(asyncio.run(main()))