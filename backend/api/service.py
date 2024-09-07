from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import psycopg2
from api.models import UserModel
from config import engine_url

async def get_user(tg_id: int):
    conn = psycopg2.connect(database="postgres", user="postgres", password="mypassword", host="db", port="5432")
    print("successfully connected")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM newtable WHERE tg_id=%s''', (tg_id,))
    value = cur.fetchone()
    return value




async def add_user(tg_id: int, username: str, fullname: str, status: int, tasks: int, session: AsyncSession):
    
    async with session:
        res = await session.scalar(select(UserModel).filter_by(tg_id=tg_id))
        if res is None:
            session.add(UserModel(tg_id=tg_id, username=username, fullname=fullname, status=status, tasks=tasks))
            await session.commit()
            return True
        return False