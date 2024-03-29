from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# 요청 객체 모델 정의
class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    content = Column(String, nullable=False)
    password = Column(String, nullable=False)

    comments = relationship("Comments", back_populates="post")


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id"))  # 외래 키
    author = Column(String, nullable=False)
    content = Column(String, nullable=False)
    password = Column(String, nullable=False)

    post = relationship("Posts", back_populates="comments")
