from sqlalchemy import Column, Integer, String, VARCHAR
from db.core import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(100), nullable=False)
    name = Column(VARCHAR(10), nullable=False)
    hashed_pw = Column(VARCHAR(100), nullable=False)
