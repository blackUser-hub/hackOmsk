import psycopg2
import asyncio
from fastapi import FastAPI


def create_users_table():

    conn = (psycopg2.connect("postgresql://postgres:mypassword@db/postgres"))
    cur = conn.cursor()
    cur.execute('''
       CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            tg_id int,
            username text,
            password text,
            status int,
            tasks int
        )
    ''')
    conn.commit()
    conn.close()

app = FastAPI()

if __name__ == "__main__":
    create_users_table()
