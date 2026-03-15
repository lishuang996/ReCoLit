import logging
import asyncio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
# --------------------------
# 1. 创建 FastAPI 实例
# --------------------------
app = FastAPI(title="用户系统", debug=True, docs_url="/docs", redoc_url="/redoc")

# --------------------------
# 2. 跨域配置
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# 3. 挂载路由
# --------------------------
try:
    from ReCoLit.backend.auth.data import users
    app.include_router(users.users_router)
    logger.info("成功挂载用户路由！")
except Exception as e:
    logger.error(f"挂载失败：{e}", exc_info=True)

# --------------------------
# 4. 自动创建数据库表 正确位置
# --------------------------
@app.on_event("startup")
async def startup_event():
    try:
        from ReCoLit.backend.auth.data.users import create_tables
        await create_tables()
        logger.info("数据库表自动创建成功！")
    except Exception as e:
        logger.error(f"创建表失败：{e}")

# --------------------------
# 5. 测试接口
# --------------------------
@app.get("/")
def root():
    return {"status": "running"}

# --------------------------
# 6. 启动服务
# --------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)