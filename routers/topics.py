from fastapi import APIRouter, Query, Response, Header
from services import topics_services, reply_services, users_service
from common import responses
from data.models import Topic, Reply
from fastapi.responses import JSONResponse
from common.auth import get_user_or_raise_401


topics_router = APIRouter(prefix='/topics')


@topics_router.get('/')
def get_topics(name: str | None = None):
    return topics_services.get_all(name)


@topics_router.get('/{id}')
def get_topics_by_id(id: int):
    topic = topics_services.get_by_id(id)

    return topic or responses.NotFound


@topics_router.get('/category_id/{category_id}')
def get_topics_by_category_id(category_id: int):
    topics = topics_services.get_by_category_id(category_id)

    return topics or responses.NotFound


@topics_router.post('/', status_code=201)
def create_topic(topic: Topic, x_token: str = Header()):
    get_user_or_raise_401(x_token)
    data = users_service.decode_token(x_token)
    if topics_services.title_exists(topic.title):
        return JSONResponse(status_code=409, content={'detail': 'Title must be unique!'})

    return topics_services.create(topic, data.get("id"))


@topics_router.post('/{topic_id}/reply')
def create_reply(reply: Reply, topic_id: int,  x_token: str = Header()):
    get_user_or_raise_401(x_token)
    data = users_service.decode_token(x_token)
    return reply_services.create_reply(reply, topic_id, data.get("id"))
