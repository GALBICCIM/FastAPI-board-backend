from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException
from typing import List


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


class UserRequest(BaseModel):
    email: EmailStr
    name: str
    phone: str
    password: str

    # 유효성 검사
    @validator("email", "name", "phone", "password")
    def check_empty(cls, v):
        if not v or v.isspace():
            raise HTTPException(status_code=422, detail="필수 항목을 입력해 주세요.")

        return v

    @validator("phone")
    def check_phone(cls, v):
        phone = v

        if "-" not in v or len(phone) != 13:
            raise HTTPException(
                status_code=422, detail="올바른 형식의 번호를 입력해 주세요."
            )

        return phone

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(
                status_code=422, detail="비밀번호는 8자리 이상으로 입력해 주세요."
            )

        return v
