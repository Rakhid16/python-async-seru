import asyncio

from time import time
from functools import lru_cache

import aiohttp
import asyncpg

@lru_cache(maxsize=32)
async def main() -> None:
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="ikal",
        password="password",
        database="postgres")

    data = await conn.fetch('select * from users;')
    print(len(data))

    await conn.executemany("INSERT INTO users(name) VALUES($1);",
                           list(zip([i['name'] for i in data])))
    await conn.executemany("INSERT INTO pengguna(name) VALUES($1);",
                           list(zip([i['name'] for i in data])))

    await conn.close()

start_time = time()
asyncio.run(main())
end_time = time()

print("--- %s seconds ---" % (end_time - start_time))