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


from models.tasks_methods import task_add, tasks_get, task_get, task_delete, user_tasks_get
from models.auth_methods import authenticate_user, create_access_token, get_password,\
    verify_password_hash
from models.user_methods import get_user, user_update, user_add, user_delete, users_get
from models.matchmaking_methods import adding_to_staging, delete_from_staging
from models.game_methods import add_to_game, leave_game, make_try