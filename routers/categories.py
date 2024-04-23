from fastapi import APIRouter, Query, Response
from services import categories_service
from common import responses

categories_router = APIRouter(prefix='/category')


@categories_router.get('/')
def get_categories(name: str | None = None):
    return categories_service.get_all(name)

@categories_router.get('/{id}')
def get_category_by_id(id:int):
    category = categories_service.get_by_id(id)

    return category or responses.NotFound

