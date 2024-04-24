from fastapi import FastAPI
from routers.topics import topics_router
from routers.categories import categories_router

print("Forum program")
app = FastAPI()
app.include_router(topics_router)
app.include_router(categories_router)