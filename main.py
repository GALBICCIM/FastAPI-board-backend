from fastapi import FastAPI
from pydantic import BaseModel
from database import AsyncSessionLocal
from model import Posts


app = FastAPI()

class PostRequest(BaseModel):
   title: str
   author: str


@app.post("/posts/")
async def reqPosts(post: PostRequest):
   async with AsyncSessionLocal() as session:
      try:
         # 새로운 게시물 객체 만들기
         new_post = Posts(title=post.title, author=post.author)
            
         # 세션에 객체 넣기
         session.add(new_post)
            
         # 데이터베이스에 커밋하기
         await session.commit()