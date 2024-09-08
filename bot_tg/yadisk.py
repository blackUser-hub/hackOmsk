#pip install yadisk-async

import yadisk_async
import asyncio
import os
from config import yatoken

y = yadisk_async.YaDisk(token=yatoken)


async def upload(y, filename: str):
             await y.upload(filename, f"/hackOmsk/{filename}")
            

async def download(y, filename: str, path2Save: str):
        await y.download(f'/hackOmsk/{filename}', path2Save)
    



async def download_by_link(y, link:str, path2Save:str):
        await y.download_by_link(link, path2Save)



async def close(y):
    await y.close()

async def  get_download_link(y, path2file_yandex):
        return await y.get_download_link(path2file_yandex)


