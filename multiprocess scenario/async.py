import asyncio

from functools import lru_cache
from multiprocessing import Pool
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
    p = Pool(processes=30)
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="ikal",
        password="password",
        database="postgres")

    data = p.map(get_pokemon, [i for i in range(1, 899)])
    p.close()

    await conn.executemany("INSERT INTO users (name) VALUES ($1)", list(zip(data)))
    await conn.executemany("INSERT INTO pengguna (name) VALUES ($1)", list(zip(data)))

    await conn.close()

start_time = time()
asyncio.run(main())
end_time = time()

print("--- %s seconds ---" % (end_time - start_time))
