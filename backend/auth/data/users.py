from fastapi import APIRouter
from sqlalchemy import String, Integer
from .database import Base, engine
from sqlalchemy.orm import Mapped, mapped_column
from .OrmTopydantic import orm_to_pydantic

class Users(Base):
    __tablename__ = "users"
    users_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")

    # 完全对应你的前端
    nick_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="用户昵称")
    real_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="真实姓名")
    sex: Mapped[str] = mapped_column(String(10), nullable=False, comment="性别：male/female/unknown")
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, comment="手机号")
    verify_code: Mapped[str] = mapped_column(String(10), nullable=False, comment="验证码")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

users_router = APIRouter(
    tags=["用户注册与登录"],
    responses={404: {"description": "用户不存在"}}
)

UsersCreate = orm_to_pydantic(Users, model_type="create")
UsersResponse = orm_to_pydantic(Users, model_type="response")
from . import UsersCRUD