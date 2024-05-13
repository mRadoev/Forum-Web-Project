from pydantic import BaseModel, constr, conint, Field
from typing import Optional
from datetime import datetime


class Category(BaseModel):
    id: int | None
    name: constr(min_length=1)
    type: constr(pattern='^private|public$')
    topics: list = []

    @classmethod
    def from_query_result(cls, id, name, is_public, topics=None):
        return cls(
            id=id,
            name=name,
            type='public' if is_public else 'private',
            topics=topics or []
        )


class Topic(BaseModel):
    id: int | None = None
    title: constr(min_length=1)
    description: constr(min_length=1)
    category_id: str | int
    replies: list = []
    best_reply: list = []

    @classmethod
    def from_query_result(cls, id, title, description, category_id, replies=None, best_reply=None):
        return cls(
            id=id,
            title=title,
            description=description,
            category_id=category_id,
            replies=replies or [],
            best_reply=best_reply or []
        )


class Reply(BaseModel):
    id: Optional[int] = None
    name: constr(min_length=1)
    description: constr(min_length=1)
    topics_id: Optional[int] = None
    votes: list = []

    @classmethod
    def from_query_result(cls, id, name, topics_id, description, votes=None):
        return cls(
            id=id,
            name=name,
            description=description,
            topics_id=topics_id,
            votes=votes or []
        )


class Vote(BaseModel):
    type: conint(ge=0, le=1)

    @classmethod
    def from_query_result(cls, likes, dislikes):
        return cls(
            likes=likes,
            dislikes=dislikes
        )


class LoginData(BaseModel):
    username: str
    password: str
    email: str


class User(BaseModel):
    id: int | None
    username: str
    password: str
    email: str


    @classmethod
    def from_query_result(cls, id, username, password, email):
        return cls(
            id=id,
            username=username,
            password=password,
            email=email)


class Conversation(BaseModel):
    user1_id: int
    user2_id: int


class Message(BaseModel):
    message_id: int | None = None
    sender_id: int
    recipient_id: int
    message_text: str

    @classmethod
    def from_query_result(cls, message_id, sender_id, recipient_id, message_text):
        return cls(
            message_id=message_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_text=message_text)


class MessagePayload(BaseModel):
    recipient_id: int
    message_text: str

