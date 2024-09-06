from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
import db

class User(db.Base):
    __tablename__ = "newtable"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    tg_id = Column(Integer)
    username = Column(String)
    fullname = Column(String)
    status = Column(Integer)
    tasks = Column(Integer)

