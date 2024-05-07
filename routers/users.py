from fastapi import APIRouter, Header
from common.responses import BadRequest
from data.models import LoginData
from services import users_service
from common.auth import get_user_or_raise_401

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


# @users_router.get('/info')
# def user_info(x_token: str = Header()):
#     return get_user_or_raise_401(x_token)