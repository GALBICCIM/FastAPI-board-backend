from fastapi import FastAPI, HTTPException
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
         new_post = Posts(title=post.title, author=post.author)  # 새로운 게시물 객체 만들기
         session.add(new_post)  # 세션에 객체 넣기
         await session.flush()

         await session.commit()  # 데이터베이스에 커밋하기
         
         return {
            "message": "POST 요청 정상 처리"
         }
      except Exception as e:  # 예외 처리
         await session.rollback()
         raise HTTPException(
            status_code=500,
            detail = f"POST 요청 실패: {str(e)}"
         )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
