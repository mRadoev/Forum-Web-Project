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
    category_id: str | int

    @classmethod
    def from_query_result(cls, id, title, description, category_id):
        return cls(
            id=id,
            title=title,
            description=description,
            category_id=category_id
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
