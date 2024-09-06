import asyncio
import typer
import uvicorn
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
import api.db as db
import api.service as service
from contextlib import asynccontextmanager
from config import BACKEND_HOST, BACKEND_PORT



cli = typer.Typer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

class UserSchema(BaseModel):
    username: str
    tg_id: int
    fio: str
    status: int
    fullname: str


@cli.command()
def db_init_models():
    asyncio.run(db.init_models())
    print("Done")


@app.get("/users/get_user/{tg_id}", response_model=list[UserSchema])
async def get_user(tg_id: int, session: AsyncSession = Depends(db.get_session)):
    user = await service.get_user(session, tg_id)
    return user


@app.post("/users/add_user")
async def add_city(user: UserSchema, session: AsyncSession = Depends(db.get_session)):
    user = service.add_user(session, user.tg_id, user.username, user.fullname, user.status, user.tasks)
    try:
        await session.commit()
        return user
    except IntegrityError as ex:
        await session.rollback()
        


if __name__ == "__main__":
    cli()
    uvicorn.run("app.main:app", reload=True, host=BACKEND_HOST, port=int(BACKEND_PORT))