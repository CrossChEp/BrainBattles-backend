"""
Module for all models in api

Functions:
    task_add
        adds task to database
    tasks_get
        gets all tasks
    task_get
        gets task using it's id
    task_delete
        deletes task using it's id
    user_tasks_get
        gets all tasks that user has ever created
    get_user
        gets user using his id
    user_update
        updates user using his id
    users_get
        gets all users
    adding_to_staging
        adds user to queue
    delete_from_staging
        deletes user from queue
    add_to_game
        adds user to the game
    leave_game
        deletes user from game
    make_try
        makes try


"""


from core.models.tasks.tasks_methods import task_add, tasks_get, get_task_by_id, user_tasks_get, update_task_data,\
    get_all_tasks_from_database, get_concrete_task_with_every_state
from core.models.auth.auth_methods import authenticate_user, create_access_token, get_password,\
    verify_password_hash
from core.models.user.user import User, UserState
from core.models.user.user_methods import get_user, update_user_data, add_user_to_database, delete_user_from_database, users_get,\
    get_user_by_id
from core.models.matchmaking.matchmaking_methods import adding_to_staging, delete_from_staging
from core.models.game.game_methods import add_to_game, leave_game, make_try
from core.models.game.game_auxiliary_methods import winner_check
from core.models.images.image_methods import decode_image, encode_image
from .general_methods import model_without_nones
from core.models.admin.users.admin_users_methods import unban_user, ban_user_temporary,\
    ban_user_permanently
