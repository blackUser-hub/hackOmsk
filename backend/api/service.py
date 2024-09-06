from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import api.models as models


async def get_user(session: AsyncSession,tg_id:int) -> list[models.User]:
    result = await session.execute(select(models.User).where(models.User.tg_id==tg_id))
    return result.scalars().all()


async def add_user(session: AsyncSession, tg_idd: int, usernamee: str, fullnamee: str, statuss: int, taskss: int):
    new_User = models.User(tg_id=tg_idd ,name=usernamee, fullname=fullnamee, status=statuss, tasks=taskss)
    session.add(new_User)
    await session.commit()
    return new_User