from fastapi import APIRouter, Depends
from task.schemas import Contacts
from task.deps import get_redis
from fastapi import HTTPException
#import aioredis

task_router = APIRouter()



@task_router.post('/write_data')
async def write_data(data: Contacts, redis=Depends(get_redis)):
    """запись в Redis"""
    if await redis.exists(data.phone):
        print('1')
        raise HTTPException(
            status_code=404, detail="такой номер телефона уже существует")
    await redis.set(data.phone, data.address)
    return  {"phone": data.phone, "address": data.address}#{"message": "данные сохранены"}


@task_router.get('/check_data')
async def check_data(phone: str, redis=Depends(get_redis)):
    """Получение данных по номеру телефона"""
    address = await redis.get(phone)
    if address is None:
        raise HTTPException(status_code=404, detail="не найдено")
    return {"phone": phone, "address": address}


@task_router.put('/update_data')
async def update_data(data: Contacts, redis=Depends(get_redis)):
    """Обновление данных"""
    if await redis.exists(data.phone):
        await redis.set(data.phone, data.address)
        return {"message": "данные обновлены"}
    else:
        raise HTTPException(status_code=404, detail="не найдено")
