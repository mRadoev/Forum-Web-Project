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

    @classmethod
    def from_query_result(cls, id, title, description, category_id, replies=None):
        return cls(
            id=id,
            title=title,
            description=description,
            category_id=category_id,
            replies=replies or []
        )


class Reply(BaseModel):
    id: Optional[int] = None
    name: constr(min_length=1)
    description: constr(min_length=1)
    topics_id: Optional[int] = None

    @classmethod
    def from_query_result(cls, id, name, topics_id, description):
        return cls(
            id=id,
            name=name,
            description=description,
            topics_id=topics_id,
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

    # def is_admin(self):
    #     return self.role == Role.ADMIN

    @classmethod
    def from_query_result(cls, id, username, password, email):
        return cls(
            id=id,
            username=username,
            password=password,
            email=email)


class Message:
    def __init__(self, id: int, sender_id: int, recipient_id: int, message: str, timestamp: datetime):
        self.id = id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.message = message
        self.timestamp = timestamp

    @classmethod
    def from_query_result(cls, id: int, sender_id: int, recipient_id: int, message: str, timestamp: datetime):
        return cls(id, sender_id, recipient_id, message, timestamp)

    def __repr__(self):
        return f"Message(id={self.id}, sender_id={self.sender_id}, recipient_id={self.recipient_id}, message={self.message}, timestamp={self.timestamp})"