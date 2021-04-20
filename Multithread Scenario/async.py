import asyncio

from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from time import time

import requests
import asyncpg


@lru_cache(maxsize=32)
def get_pokemon(number: int) -> str:
    pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{number}')
    pokemon = pokemon.json()['name']

    print(pokemon)

    return pokemon


async def main() -> None:
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="ikal",
        password="password",
        database="postgres")

    with ThreadPoolExecutor(max_workers=898) as executor:
        data = [executor.submit(get_pokemon, i) for i in range(1, 899)]

    data = [hasil.result() for hasil in data]

    await conn.executemany("INSERT INTO users (name) VALUES ($1)", list(zip(data)))
    await conn.executemany("INSERT INTO pengguna (name) VALUES ($1)", list(zip(data)))

    await conn.close()

start_time = time()
asyncio.run(main())
end_time = time()

print("--- %s seconds ---" % (end_time - start_time))
