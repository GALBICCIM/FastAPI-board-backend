from fastapi import FastAPI, HTTPException
from db.core import *
from db.schema import *
from db.posts import Posts
from db.comments import Comments
from db.users import Users
from sqlalchemy.future import select

from passlib.context import CryptContext


app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# GET 모든 글 불러오기 엔드포인트
@app.get("/posts/")
async def getAllPosts():
    async with AsyncSessionLocal() as session:
        posts_list = []
        comments_list = []

        posts_result = await session.execute(
            select(Posts)
        )  # 모든 데이터를 가져오는 쿼리문
        posts = posts_result.scalars().all()

        for post in posts:
            comments_result = await session.execute(
                select(Comments).filter(Comments.post_id == post.id)
            )
            comments = comments_result.scalars().all()

            for comment in comments:
                comments_list.append(
                    {
                        "id": comment.id,
                        "author": comment.author,
                        "content": comment.content,
                    }
                )

            posts_list.append(
                {
                    "id": post.id,
                    "title": post.title,
                    "author": post.author,
                    "content": post.content,
                    "comments": comments_list,
                }
            )

        page_count = len(posts_list)

        return {"page_count": page_count, "posts": posts_list}


# GET 특정 글 불러오기 엔드포인트
@app.get("/posts/{post_id}")
async def getPost(post_id: int):
    async with AsyncSessionLocal() as session:
        comments_list = []
        post_result = await session.execute(
            select(Posts).filter(Posts.id == post_id)
        )  # 글 쿼리문
        post = post_result.scalars().first()

        comments_result = await session.execute(
            select(Comments).filter(Comments.post_id == post.id)
        )
        comments = comments_result.scalars().all()

        for comment in comments:
            comments_list.append(
                {
                    "id": comment.id,
                    "author": comment.author,
                    "content": comment.content,
                }
            )

        return {
            "post": {
                "id": post_id,
                "title": post.title,
                "author": post.author,
                "content": post.content,
                "comments": comments_list,
            }
        }


# POST 계정 생성 엔드포인트
@app.post("/users/")
async def reqUser(user: UserRequest):
    async with AsyncSessionLocal() as session:
        # email이 같은 유저 정보 불러오기
        user_info = await session.query(Users).filter(Users.email == user.email).first()

        # 유저 존재 확인
        if user_info:
            raise HTTPException(status_code=409, detail="유저가 이미 존재합니다.")

        try:
            new_user = Users(
                name=user.name,
                email=user.email,
                hashed_pw=pwd_context.hash(user.password),  # 비밀번호 해시
            )

            session.add(new_user)
            await session.commit()

            return {"user_id": new_user.id}
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"계정 생성 실패: {str(e)}")


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


# DELETE 댓글 삭제 엔드포인트
@app.delete("/posts/{post_id}/comments/{comment_id}")
async def delComment(post_id: int, comment_id: int, password: str):
    async with AsyncSessionLocal() as session:
        posts_result = await session.execute(
            select(Posts).filter(Posts.id == post_id)
        )  # 모든 데이터를 가져오는 쿼리문
        post = posts_result.scalars().first()

        comments_result = await session.execute(
            select(Comments).filter(
                and_(Comments.post_id == post_id, Comments.id == comment_id)
            )
        )
        comment = comments_result.scalars().first()

        if post is None or comment is None:
            raise HTTPException(
                status_code=404, detail="게시물 또는 댓글을 찾을 수 없습니다."
            )

        if comment.password != password:
            return {"ok": False}

        await session.delete(comment)
        await session.commit()

        return {"ok": True}
