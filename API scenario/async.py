import asyncio

from functools import lru_cache
from time import time

import aiohttp
import asyncpg

@lru_cache(maxsize=32)
async def get_pokemon(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as resp:
        pokemon = await resp.json()
        print(pokemon['name'])

        return pokemon['name']

@lru_cache(maxsize=32)
async def main() -> None:
    # DB Connection
    conn = await asyncpg.connect(
        host="localhost",
        port=0000,
        user="postgres",
        password="password",
        database="ngoding_bebas")

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(get_pokemon(session,
                 f'https://pokeapi.co/api/v2/pokemon/{number}')) for number in range(1, 151)]

        original_pokemon = await asyncio.gather(*tasks)
        await conn.executemany("INSERT INTO users(name) VALUES($1);",
                               list(zip(original_pokemon)))

    await conn.close()

start_time = time()
asyncio.run(main())
end_time = time()

print("--- %s seconds ---" % (end_time - start_time))