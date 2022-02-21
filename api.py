import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api_routers import auth_router, tasks_router
from api_routers.users import users_router

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:63343",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(tasks_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)