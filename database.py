from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


# {SQL}://{USER}:{PASSWORD}@{HOST}:{PORT}/{SCHEMA NAME}
DB_URL = "mysql+aiomysql://root:park3683@localhost:3306/anonymous_board"

async_engine = create_async_engine(DB_URL)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)
