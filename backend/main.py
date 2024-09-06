import asyncio, uvicorn
import typer
from typer import Typer
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
from config import BACKEND_HOST, BACKEND_PORT
from api.routers.router import router
from contextlib import asynccontextmanager
import asyncio

cli = Typer()
@cli.command()
def db_init_models():
    asyncio.run(db.init_models())
    uvicorn.run("main:app", reload=True, host=BACKEND_HOST, port=int(BACKEND_PORT))
    print("Done")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # asyncio.create_task(transactions_listener())
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(router)

if __name__ == "__main__":
    cli()
    