from fastapi import APIRouter, Depends
from task.schemas import Contacts
from task.deps import get_redis
from fastapi import HTTPException
from fastapi import Request
#import aioredis

task_router = APIRouter()



@task_router.post('/write_data')
@task_router.put('/write_data')
async def write_data(request: Request, data: Contacts, redis=Depends(get_redis)):
    """запись и обновление данных в Redis"""
    if request.method == 'POST':
        if await redis.exists(data.phone):
            print('1')
            raise HTTPException(
                status_code=404, detail="такой номер телефона уже существует")
        await redis.set(data.phone, data.address)
        return  {"phone": data.phone, "address": data.address}
    if request.method == 'PUT':
        # обновление данных
        if await redis.exists(data.phone):
            await redis.set(data.phone, data.address)
            return {"message": "данные обновлены"}
        else:
            raise HTTPException(status_code=404, detail="не найдено")



@task_router.get('/check_data')
async def check_data(phone: str, redis=Depends(get_redis)):
    """Получение данных по номеру телефона"""
    address = await redis.get(phone)
    if address is None:
        raise HTTPException(status_code=404, detail="не найдено")
    return {"phone": phone, "address": address}


"""
@task_router.put('/update_data')
async def update_data(data: Contacts, redis=Depends(get_redis)):
    if await redis.exists(data.phone):
        await redis.set(data.phone, data.address)
        return {"message": "данные обновлены"}
    else:
        raise HTTPException(status_code=404, detail="не найдено")
"""
