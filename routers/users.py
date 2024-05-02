from fastapi import APIRouter
from common.responses import BadRequest
from data.models import LoginData
from services import users_service

users_router = APIRouter(prefix='/users')


@users_router.post('/login')
def login(data: LoginData):
    user = users_service.try_login(data.username, data.password)

    if user:
        token = users_service.create_token(user)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')


@users_router.post('/register')
def register(data: LoginData):
    user = users_service.create(data.username, data.password, data.email)

    return user or BadRequest(f'Username {data.username} is taken.')
