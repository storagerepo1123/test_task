import aioredis
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from task.routes import task_router
from config import REDIS_HOST, REDIS_PORT

# для win
#REDIS_HOST = REDIS_HOST
#REDIS_PORT = REDIS_PORT
#REDIS_PASS = 'foobared' #в win в конфигах redis доступ по паролю
# для lin
REDIS_HOST = REDIS_HOST
REDIS_PORT = REDIS_PORT


def create_app(redis=None):
    """создания приложения FastAPI, 
       подключение к Redis при старте сервера
    """
    app = FastAPI()
    app.include_router(task_router)

    @app.on_event('startup')
    async def startup():

        nonlocal redis

        if redis is None:
            redis = await aioredis.from_url(
                f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True
            )
        assert await redis.ping()

    @app.middleware('http')
    async def http_middleware(request: Request, call_next):
        nonlocal redis

        err = {'error': True, 'message': "ошибка сервера"},
        response = JSONResponse(err, status_code=500)

        try:
            # объявляю о состоянии redis
            request.state.redis = redis
            response = await call_next(request)
        finally:
            return response

    return app
