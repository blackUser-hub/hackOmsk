import asyncio
import typer
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
import api.db as db
import api.service as service
from fastapi import APIRouter 
from sqlalchemy import select 
from api.models import User

app = FastAPI()
router = APIRouter(prefix='/users', tags=['Работа с пользователями'])


class UserSchema(BaseModel):
    username: str
    tg_id: int
    fio: str
    status: int
    fullname: str


@router.get("/get_user/{tg_id}", summary="Получить пользователя", response_model=list[UserSchema])
async def get_user(tg_id: int):
    async with db.async_session_maker() as session: 
        query = select(User).where(tg_id=tg_id)
        result = await session.execute(query)
        students = result.scalars().all()
        return students

@router.post("/add_user", summary="Добавить пользователя")
async def add_city(user: UserSchema, session: AsyncSession = Depends(db.get_session)):
    user = service.add_user(session, user.tg_id, user.username, user.fullname, user.status, user.tasks)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        


app.include_router()