import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api_routers import auth_router, tasks_router, matchmaking_router, game_router
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


@app.get('/')
def index():
    return {'info': 'server started'}


app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(matchmaking_router)
app.include_router(game_router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)