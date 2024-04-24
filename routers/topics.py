from fastapi import APIRouter, Query, Response
from services import topics_services
from common import responses
from data.models import Topic
from fastapi.responses import JSONResponse

topics_router = APIRouter(prefix='/topics')

@topics_router.get('/')
def get_topics(name: str | None = None):
    return topics_services.get_all(name)

@topics_router.get('/{id}')
def get_topics_by_id(id: int):
    topic = topics_services.get_by_id(id)

    return topic or responses.NotFound

@topics_router.post('/', status_code=201)
def create_topic(topic: Topic):
    if topics_services.title_exists(topic.title):
        return JSONResponse(status_code=409, content={'detail': 'Title must be unique!'})

    return topics_services.create(topic)