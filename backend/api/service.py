from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import api.models as models


async def get_user(session: AsyncSession,tg_id:int) -> list[models.User]:
    result = await session.execute(select(models.User).where(models.User.tg_id==tg_id))
    return result.scalars().all()


async def add_user(session: AsyncSession, tg_idd: int, usernamee: str, fullnamee: str, statuss: int, taskss: int):
    async with session:
        res = await session.scalar(select(models.User).filter_by(tg_id=tg_idd))
        if res is None:
            session.add(models.User(tg_id=tg_idd, username=usernamee, fullname=fullnamee, status=statuss, tasks=taskss))
            await session.commit()
            return True
        return False