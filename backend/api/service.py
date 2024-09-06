from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import api.models as models


async def get_user(session: AsyncSession,tg_id:int) -> list[models.User]:
    result = await session.execute(select(models.User).where(models.User.tg_id==tg_id))
    return result.scalars().all()


async def add_user(session: AsyncSession, tg_id: int, username: str, fullname: str, status: int, tasks: int):
    new_User = models.User(tg_id=tg_id,name=username, fullname=fullname, status=status, tasks=tasks)
    session.add(new_User)
    return new_User