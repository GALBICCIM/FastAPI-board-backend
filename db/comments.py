from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.core import Base
# from posts import Posts


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id"))  # 외래 키
    author = Column(String, nullable=False)
    content = Column(String, nullable=False)
    password = Column(String, nullable=False)

    post = relationship("Posts", back_populates="comments")
