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

from core.schemas.user_models import UserRegisterModel, UserGetModel, UserUpdateModel,\
    UserAbstractModel, BanUserModel, UserUpdateAdminModel
from core.schemas.game_models import GameModel
from core.schemas.queue_models import QueueModel
from core.schemas.tasks_models import TaskAddModel, TaskUpdateModel, TaskGetModel
from core.schemas.token_models import Token, TokenData
