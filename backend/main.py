import psycopg2
import asyncio
from fastapi import FastAPI
from config import engine_url


def create_users_table():

    conn = (psycopg2.connect(engine_url))
    cur = conn.cursor()
    cur.execute('''
       CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            tg_id bigint,
            username text,
            password text,
            status bigint,
            tasks bigint
        )
    ''')
    conn.commit()
    conn.close()
def create_tasks_table():

    conn = (psycopg2.connect(engine_url))
    cur = conn.cursor()
    cur.execute('''
       CREATE TABLE IF NOT EXISTS tasks(
            id SERIAL PRIMARY KEY,
            tg_id bigint,
            yandexgpt_text text,
            audio_path text,
            output_csv_path text,
            otchet_docx_path text,
            otchet_pdf_path text,
            transcript_docx_path text,
            status bigint default 0
        )
    ''')
    conn.commit()
    conn.close()

app = FastAPI()

if __name__ == "__main__":
    create_users_table()
    create_tasks_table()