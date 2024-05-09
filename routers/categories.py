from fastapi import APIRouter, Query, Response
from services import categories_service
from common import responses
from data.models import Category
from fastapi.responses import JSONResponse

categories_router = APIRouter(prefix='/category')


@categories_router.get('/')
def get_categories(name: str | None = None):
    return categories_service.get_all(name)


@categories_router.get('/{id}')
def get_category_by_id(id: int):
    category = categories_service.get_by_id(id)

    return category or responses.NotFound


@categories_router.post('/', status_code=201)
def create_category(category: Category):

    if categories_service.name_exists(category.name):
        return JSONResponse(status_code=409, content={'detail': 'Category name must be unique!'})

    return categories_service.create(category)
