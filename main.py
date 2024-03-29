from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import *
from model import Posts
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


app = FastAPI()

class PostRequest(BaseModel):
   title: str
   author: str
   content: str
   password: int
   
# class DeleteRequest(BaseModel):
#    post_id: int
#    password: int


# GET 특정 글 불러오기 엔드포인트
@app.get("/posts/{post_id}")
async def getPost(post_id: int):
   async with AsyncSessionLocal() as session:
        result = await session.execute(select(Posts).filter(Posts.id == post_id))
        post_info = result.scalars().first()
        
        return {
            "ok": True,
            "data": post_info
        }

# POST 글 작성 엔드포인트
@app.post("/posts/")
async def reqPost(post: PostRequest):
   async with AsyncSessionLocal() as session:
      try:
         new_post = Posts(
            title = post.title,
            author = post.author,
            content = post.content,
            password = post.password
         )  # 새로운 게시물 객체 만들기
         session.add(new_post)  # 세션에 객체 넣기
         await session.flush()

         await session.commit()  # 데이터베이스에 커밋하기
         
         return {
            "post_id": new_post.id  # new_post의 id를 반환
         }
      except Exception as e:  # 예외 처리
         await session.rollback()
         raise HTTPException(
            status_code=500,
            detail = f"POST 요청 실패: {str(e)}"
         )


# DELETE 글 삭제 엔드포인트
@app.delete("/posts/{post_id}")
async def delPost(post_id: int, password: int):
   async with AsyncSessionLocal() as session:
      post = await session.get(Posts, post_id)  # 게시물 불러오기 [parameter: (model, PRIMARY KEY)]
      # 게시물이 있는지 확인
      if post is None:
         raise HTTPException(status_code = 404, detail="게시물을 찾을 수 없습니다.")
      
      # 게시물 비밀번호와 삭제할 게시물 비밀번호가 일치한지 확인
      if post.password != password:
         return {"ok": False}

      await session.delete(post)
      await session.commit()
      
      return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
