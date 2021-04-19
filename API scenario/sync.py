from functools import lru_cache
from time import time

import requests
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="ikal",
    database="ngoding_bebas")
cursor = conn.cursor()


@lru_cache(maxsize=32)
def get_pokemon(url: str) -> str:
    pokemon = requests.get(url)
    pokemon = pokemon.json()

    print(pokemon['name'])

    return pokemon['name']


@lru_cache(maxsize=32)
def main() -> None:
    tasks = [get_pokemon(
        f'https://pokeapi.co/api/v2/pokemon/{number}') for number in range(1, 899)]

    args_str = b','.join(cursor.mogrify("%s", (x, )) for x in list(zip(tasks)))
    args_str = [i.replace("(", "").replace("'", "").replace(")", "")
                for i in args_str.decode("utf-8").split(",")]

    cursor.executemany("INSERT INTO users (name) VALUES (%s)",
                       list(zip(args_str)))
    conn.commit()

    conn.close()


start_time = time()
main()
end_time = time()

print("--- %s seconds ---" % (end_time - start_time))
