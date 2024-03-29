from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import *
from model import Posts, Comments
from sqlalchemy.future import select
from typing import List


app = FastAPI()


class PostRequest(BaseModel):
    title: str
    author: str
    content: str
    password: str
    comments: List[str] = []  # 배열 초기화


class CommentRequest(BaseModel):
    author: str
    content: str
    password: str


# class DeleteRequest(BaseModel):
#    post_id: int
#    password: int


# GET 모든 글 불러오기 엔드포인트
@app.get("/posts/")
async def getAllPosts():
    async with AsyncSessionLocal() as session:
        # posts_list = []
        # result = await session.execute(select(Posts))  # 모든 데이터를 가져오는 쿼리문
        # posts = result.scalars().all()

        # for post in posts:
        #     comments_list = []
        #     comments = await session.execute(
        #         select(Comments).filter(Comments.post_id == post.id)
        #     )

        #     for comment in comments:
        #         comments_list.append(
        #             {
        #                 "id": comment.id,
        #                 "author": comment.author,
        #                 "content": comment.content,
        #             }
        #         )

        #     posts_list.append(
        #         {
        #             "id": post.id,
        #             "title": post.title,
        #             "author": post.author,
        #             "content": post.content,
        #             "comments": comments_list,
        #         }
        #     )

        # page_count = len(posts_list)

        # return {"page_count": page_count, "posts": posts_list}

        # Posts와 Comments 테이블을 조인하여 한 번의 쿼리로 모든 데이터를 가져옴
        query = select(Posts, Comments).join(Comments).order_by(Posts.id, Comments.id)
        result = await session.execute(query)
        posts_with_comments = result.scalars().all()

        posts_list = []
        current_post = None
        for post, comment in posts_with_comments:
            # 새로운 게시물에 도달하면 이전 게시물을 결과 리스트에 추가
            if current_post is None or current_post.id != post.id:
                if current_post is not None:
                    posts_list.append(current_post)
                current_post = {
                    "id": post.id,
                    "title": post.title,
                    "author": post.author,
                    "content": post.content,
                    "comments": [],
                }
            # 현재 댓글을 현재 게시물에 추가
            current_post["comments"].append(
                {"id": comment.id, "author": comment.author, "content": comment.content}
            )

        # 마지막 게시물을 결과 리스트에 추가
        if current_post is not None:
            posts_list.append(current_post)

        page_count = len(posts_list)
        return {"page_count": page_count, "posts": posts_list}


# GET 특정 글 불러오기 엔드포인트
@app.get("/posts/{post_id}")
async def getPost(post_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Posts).filter(Posts.id == post_id)
        )  # 글 쿼리문
        post_info = result.scalars().first()

        comments = await session.execute(
            select(Comments).filter(Comments.post_id == post_info.id)
        )  # 모든 댓글 불러오기
        comments_list = [
            comment.content for comment in comments.scalars().all()
        ]  # 댓글 리스트에 넣기

        return {
            "post": {
                "id": post_id,
                "title": post_info.title,
                "author": post_info.author,
                "content": post_info.content,
                "comments": comments_list,
            }
        }


# POST 글 작성 엔드포인트
@app.post("/posts/")
async def reqPost(post: PostRequest):
    async with AsyncSessionLocal() as session:
        try:
            new_post = Posts(
                title=post.title,
                author=post.author,
                content=post.content,
                password=post.password,
            )  # 새로운 게시물 객체 만들기
            session.add(new_post)  # 세션에 객체 넣기
            await session.flush()
            await session.commit()  # 데이터베이스에 커밋하기

            return {"post_id": new_post.id}  # new_post의 id를 반환
        except Exception as e:  # 예외 처리
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"글 작성 실패: {str(e)}")


# POST 댓글 작성 엔드포인트
@app.post("/posts/{post_id}/comments")
async def reqComment(post_id: int, comment: CommentRequest):
    async with AsyncSessionLocal() as session:
        post = await session.get(Posts, post_id)

        if post is None:
            raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

        new_comment = Comments(
            post_id=post_id,
            author=comment.author,
            content=comment.content,
            password=comment.password,
        )
        session.add(new_comment)
        await session.commit()

        return {"comment_id": new_comment.id}


# DELETE 글 삭제 엔드포인트
@app.delete("/posts/{post_id}")
async def delPost(post_id: int, password: int):
    async with AsyncSessionLocal() as session:
        post = await session.get(
            Posts, post_id
        )  # 게시물 불러오기 [parameter: (model, PRIMARY KEY)]
        # 게시물이 있는지 확인
        if post is None:
            raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

        # 게시물 비밀번호와 삭제할 게시물 비밀번호가 일치한지 확인
        if post.password != password:
            return {"ok": False}

        await session.delete(post)
        await session.commit()

        return {"ok": True}
