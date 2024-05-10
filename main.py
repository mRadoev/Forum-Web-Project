from fastapi import FastAPI
from routers.topics import topics_router
from routers.categories import categories_router
from routers.users import users_router
from routers.messages import messages_router
import uvicorn


print("Forum program")
app = FastAPI()
app.include_router(topics_router)
app.include_router(categories_router)
app.include_router(users_router)
app.include_router(messages_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
