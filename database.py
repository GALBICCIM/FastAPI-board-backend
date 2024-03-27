from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


DB_URL = "mysql://root:park3683@localhost:3306/anonymous_board"

async_engine = create_async_engine(DB_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)  
