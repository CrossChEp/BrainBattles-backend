"""
Module of api's schemas

Classes
    UserModel
        scheme of user
    Token
        scheme of token
    TokenData
        scheme of token with username
    TaskModel
        scheme of task
"""

from schemas.user_models import UserModel, UserGetModel, UserUpdate
from schemas.game_models import GameModel
from schemas.queue_models import QueueModel
from schemas.tasks_models import TaskModel, TaskUpdateModel
from schemas.token_models import Token, TokenData
