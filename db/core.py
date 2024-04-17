from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from config import settings


DB_URL = settings.DATABASE_URL

async_engine = create_async_engine(DB_URL)

AsyncSessionLocal = sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


# SQL 베이스 정의
Base = declarative_base()
