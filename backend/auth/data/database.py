"""
数据库基类，包括依赖
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func, DateTime
from .url import ASYNC_DB_URL, ENV
# 基类（所有表的公共字段）
class Base(DeclarativeBase):
    create_time:Mapped[datetime]=mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now,onupdate=func.now(),comment="修改时间")
# 初始化异步引擎
engine = create_async_engine(
    ASYNC_DB_URL,
    echo=True if ENV == "development" else False  # 开发环境打印SQL
)
# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# 数据库依赖（供接口调用）
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
