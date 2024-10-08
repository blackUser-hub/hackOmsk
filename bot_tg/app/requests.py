from config import backend_api_url
import requests
import aiohttp
import logging
import psycopg2
from typing import List, Dict, Optional
from config import engine_url

logger = logging.getLogger(__name__)


async def init_user(tg_id: int, username: str, fullname: str, status: int, tasks: int):
    conn = (psycopg2.connect(engine_url))
    cur = conn.cursor()
    cur.execute('''
       INSERT INTO users (tg_id, username, password, status, tasks) VALUES (%s, %s, %s, %s, %s)
    ''', (tg_id, username, fullname, status, tasks))
    conn.commit()
    conn.close()

async def add_task(tg_id: int, audio_path: str):
    conn = (psycopg2.connect(engine_url))
    cur = conn.cursor()
    cur.execute("""INSERT INTO tasks (tg_id, audio_path, status) VALUES(%s, %s, %s)""", (tg_id, audio_path, 1))
    conn.commit()
    conn.close()      

async def get_user(tg_id: int):
    conn = psycopg2.connect(database="postgres", user="postgres", password="mypassword", host="db", port="5432")
    print("successfully connected")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users WHERE tg_id=%s''', (tg_id,))
    user = cur.fetchone()
    try:
        data = {
             
                "tg_id": user[1],
                "username": user[2],
                "password": user[3],
                "status": user[4],
                "tasks": user[5],
                "id": user[0]
            
            }
        return data
    except TypeError:
        return {}
async def get_otchets(tg_id: int) -> List[Dict[str, Optional[str]]]:
    conn = psycopg2.connect(database="postgres", user="postgres", password="mypassword", host="db", port="5432")
    print("successfully connected")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM tasks WHERE tg_id=%s''', (tg_id,))
    otchets = cur.fetchall()
    data = []
    
    for otchet in otchets:
        data.append({
            "id": otchet[0],
            "tg_id": otchet[1],
            "yandexgpt_text": otchet[2],
            "audio_path": otchet[3],
            "output_csv_path": otchet[4],
            "otchet_docx_path": otchet[5],
            "otchet_pdf_path": otchet[6],
            "transcript_docx_path": otchet[7],
            "status": otchet[8]
        })
    
    return data

async def get_last_task_id(tg_id: int):
    conn = psycopg2.connect(database="postgres", user="postgres", password="mypassword", host="db", port="5432")
    print("successfully connected")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM tasks WHERE tg_id=%s ORDER BY id DESC LIMIT 1''', (tg_id,))
    last_task = cur.fetchone()
    return last_task[0]


async def add_output_csv_path(id:int, filename:str):
    conn = (psycopg2.connect(engine_url))
    cur = conn.cursor()
    cur.execute('''UPDATE tasks SET output_csv_path=%s, statatus=2 WHERE id=%s''', (filename, id))
    conn.commit()
    conn.close()  
async def add_all_to_task(id: int, yandexgpt_text:str, output_csv_path:str, otchet_docx_path:str, otchet_pdf_path:str, transcript_docx_path:str, status:int):
    conn = (psycopg2.connect("postgresql://postgres:mypassword@db/postgres"))
    cur = conn.cursor()
    cur.execute('''UPDATE tasks SET yandexgpt_text=%s, output_csv_path=%s, otchet_docx_path=%s, otchet_pdf_path=%s, transcript_docx_path=%s, status=%s WHERE id=%s''', (yandexgpt_text, output_csv_path, otchet_docx_path, otchet_pdf_path, transcript_docx_path, status, id))
    conn.commit()
    conn.close()  

async def get_otchet_from_id(id: int):
    conn = psycopg2.connect(database="postgres", user="postgres", password="mypassword", host="db", port="5432")
    print("successfully connected")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM tasks WHERE id=%s''', (id,))
    otchet = cur.fetchone()
    return otchet

async def post_file(filename):
    params={"file": filename}
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{backend_api_url}/file/upload-file", params=params) as res:
            if res.status == 200:
                return res.json()
            else:
                logger.warning((await res.json())['detail'])   
                return None
            

async def get_file(filename):
    params = {"filename": filename}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{backend_api_url}/file/download", params=params) as res:
            if res.status == 200:
                return True
            else:
                return False