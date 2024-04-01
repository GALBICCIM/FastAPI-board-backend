from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.core import Base
# from comments import Comments


# 요청 객체 모델 정의
class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    content = Column(String, nullable=False)
    password = Column(String, nullable=False)

    comments = relationship("Comments", back_populates="post")
