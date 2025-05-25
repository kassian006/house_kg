import fastapi
from fastapi import FastAPI
from api.endpoints import house
import redis
import uvicorn
from admin.setup import setup_admin
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from contextlib import asynccontextmanager
import redis.asyncio as redis
from starlette.middleware.sessions import SessionMiddleware
from house_app.config import SECRET_KEY
from fastapi_pagination import add_pagination


async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding="utf-8", decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()

house_app = fastapi.FastAPI(title='Car site', lifespan=lifespan)
house_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
setup_admin(house_app)
add_pagination(house_app)

house_app.include_router(house.house_router, tags=["House"])

if __name__ == "__main__":
    uvicorn.run(house_app, host="127.0.0.1", port=8001)