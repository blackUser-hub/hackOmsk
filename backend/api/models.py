from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy import String
from sqlalchemy import Integer, BigInteger
import api.db as db
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    __allow_unmpapped__ = True

    pass
    

class UserModel(Base):
    __tablename__ = "newtable"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = mapped_column(String(50))
    status: Mapped[int] = mapped_column()
    tasks: Mapped[int] = mapped_column()

