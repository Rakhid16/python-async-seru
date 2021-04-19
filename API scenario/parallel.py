from time import time
from functools import lru_cache
from multiprocessing import Pool

import requests
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="ikal",
    password="password",
    database="postgres")
cursor = conn.cursor()


@lru_cache(maxsize=32)
def get_pokemon(number: int) -> str:
    pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{number}')
    pokemon = pokemon.json()['name']
    print(pokemon)

    return pokemon


@lru_cache(maxsize=32)
def main() -> None:
    p = Pool(processes=30)

    data = p.map(get_pokemon, [i for i in range(1, 899)])
    p.close()

    cursor.executemany("INSERT INTO users (name) VALUES (%s)", list(zip(data)))
    conn.commit()

    conn.close()


start_time = time()
main()
end_time = time()

print("--- %s seconds ---" % (end_time - start_time))
