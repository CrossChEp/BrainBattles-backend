""" Module for api endpoints

    Functions:
        users_router
            router for user's endpoints
        auth_router
            router for auth endpoints
        tasks_router
            router for users endpoints
        matchmaking_router
            router for matchmaking
        game_router
            router for games
"""

from core.api_routers.users import users_router
from core.api_routers.auth import auth_router
from core.api_routers.tasks import tasks_router
from core.api_routers.matchmaking import matchmaking_router
from core.api_routers.game import game_router
from core.api_routers.admin.admin_users import admin_users_router
from core.api_routers.admin.admin_tasks import admin_task_router
