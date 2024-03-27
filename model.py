from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# SQL 베이스 정의
Base = declarative_base()

# 요청 객체 모델 정의
class Posts(Base):
   __tablename__ = "posts"

   id = Column(Integer, primary_key=True)
   title = Column(String, nullable=False)
   author = Column(String, nullable=False)
