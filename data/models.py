from pydantic import BaseModel, constr, conint, Field


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
    id: int | None
    title: constr(min_length=1)
    description: constr(min_length=1)
    categories: list = []

    @classmethod
    def from_query_result(cls,id,title,description, categories=None):
        return cls(
            id=id,
            title=title,
            description=description,
            categories=categories or [])
