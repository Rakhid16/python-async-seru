from functools import lru_cache
from time import time

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="ikal",
    password="password",
    database="postgres")
cursor = conn.cursor()


@lru_cache(maxsize=32)
def main() -> None:
    cursor.execute('select * from users;')
    data = cursor.fetchall()
    
    print(len(data))

    cursor.executemany("INSERT INTO users (name) VALUES (%s)",
                       list(zip([i[1] for i in data])))
    conn.commit()

    cursor.executemany("INSERT INTO pengguna (name) VALUES (%s)",
                       list(zip([i[1] for i in data])))
    conn.commit()

    conn.close()


start_time = time()
main()
end_time = time()

print("--- %s seconds ---" % (end_time - start_time))
