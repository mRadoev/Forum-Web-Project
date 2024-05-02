from fastapi import FastAPI
from routers.topics import topics_router
from routers.categories import categories_router
from data.database import *
import uvicorn


print("Forum program")
app = FastAPI()
app.include_router(topics_router)
app.include_router(categories_router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
