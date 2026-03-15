from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Optional

from .database import get_db
from .users import UsersResponse, Users, users_router, UsersCreate

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(pwd):
    return pwd_context.hash(pwd)

def verify_password(pwd, hashed):
    return pwd_context.verify(pwd, hashed)

# ------------------------------
# 登录（手机号+密码）
# ------------------------------
class UserLoginRequest(BaseModel):
    phone_number: str
    password: str

# ------------------------------
# 注册（含验证码）
# ------------------------------
@users_router.post("/register", response_model=UsersResponse, status_code=201)
async def register(
    user_info: UsersCreate,
    db: AsyncSession = Depends(get_db)
):
    # 检查手机号是否已注册
    res = await db.execute(select(Users).where(Users.phone_number == user_info.phone_number))
    if res.scalar_one_or_none():
        raise HTTPException(400, "该手机号已注册")

    # 密码加密
    data = user_info.model_dump()
    data["password"] = get_password_hash(data["password"])

    new_user = Users(**data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# ------------------------------
# 登录
# ------------------------------
@users_router.post("/login", response_model=UsersResponse)
async def login(
    login_info: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(select(Users).where(Users.phone_number == login_info.phone_number))
    user = res.scalar_one_or_none()

    if not user or not verify_password(login_info.password, user.password):
        raise HTTPException(401, "手机号或密码错误")

    return user

# ------------------------------
# 查询 / 修改 / 删除
# ------------------------------
@users_router.get("/{user_id}/detail", response_model=UsersResponse)
async def get_detail(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(Users, user_id)
    if not user:
        raise HTTPException(404)
    return user

@users_router.put("/{user_id}/detail", response_model=UsersResponse)
async def update_detail(user_id: int, info: UsersCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(Users, user_id)
    if not user:
        raise HTTPException(404)
    data = info.model_dump()
    data["password"] = get_password_hash(data["password"])
    for k, v in data.items():
        setattr(user, k, v)
    await db.commit()
    await db.refresh(user)
    return user

@users_router.delete("/{user_id}")
async def del_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(Users, user_id)
    if not user:
        raise HTTPException(404)
    await db.delete(user)
    await db.commit()
    return {"msg": "ok"}