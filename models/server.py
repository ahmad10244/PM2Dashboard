from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime

from app import db


class Server(db.Model):
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=True)
    url = Column(String(128), unique=True)
    createDate = Column(DateTime(), server_default=func.now())
    updateDate = Column(DateTime(), nullable=True)

    @classmethod
    def find_by_id(cls, id: int) -> "Server":
        return cls.query.filter_by(id=id).first()
