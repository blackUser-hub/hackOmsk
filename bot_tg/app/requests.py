from config import backend_api_url
import requests
import aiohttp
import logging

logger = logging.getLogger(__name__)


async def init_user(tg_id, fio, username, status, tasks):
    params = {"tg_id": tg_id, "username": username, "name": fio, "status": status, "tasks": tasks}
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{backend_api_url}/users/add_user', params=params) as res:  
            if res.status == 200:
                return True
            else:
                logger.warning((await res.json())['detail'])   
                return False
            

async def get_user(tg_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{backend_api_url}/users/get_user/{tg_id}") as res:
            if res.status == 200:
                return res.json()
            else:
                logger.warning((await res.json())['detail'])   
                return None