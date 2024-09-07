import asyncio, uvicorn
import typer
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import IntegrityError
import api.db as db
import api.service as service
from fastapi import APIRouter, UploadFile, File
from sqlalchemy import select 
from api.models import UserModel
import logging
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import BigInteger, String, text, LargeBinary, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Type, Union, Iterable

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/users', tags=['Работа с пользователями'])
router_files = APIRouter(prefix='/file')


@router_files.get("/download")
def download_file(filename: str):
    return FileResponse(path=filename, filename=filename)

@router_files.post("/upload-file")
def upload_file(file: UploadFile):
    return {"filename": file.filename}


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class Base_val(AsyncAttrs, DeclarativeBase):
    pass





class AddUser_schema(Base):
    pass

class UserBase(BaseModel):
    tg_id: int
    username: str
    fullname: str
    

class User(UserBase):
    id: int
    status: int
    tasks: int
    


class User_schema(Base):
    data: User = None

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get('/{tg_id}', response_model=User)
async def get_user_info(tg_id: int):
    try:
        user = await service.get_user(tg_id)
    except Exception as e:
        logger.error(f'Internal server error: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')
    if user != ():
        
        data = {
             
                "tg_id": user[1],
                "username": user[2],
                "fullname": user[3],
                "status": user[4],
                "tasks": user[5],
                "id": user[0]
            
        }
        return data
        
    else:
        raise HTTPException(status_code=400, detail="User wasn't found")



@router.post('/initialize', response_model=AddUser_schema)
async def initialize_user(tg_id: int, username: str, fullname: str, status: int, tasks: int, session: AsyncSession = Depends(db.get_session)):
    try:
        success = await service.add_user(tg_id, username, fullname, status, tasks, session)
    except Exception as e:
        logger.error(f'Internal server error: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')

    if success:
        return AddUser_schema()
    else:
        raise HTTPException(status_code=400, detail='The user has already been initialized')