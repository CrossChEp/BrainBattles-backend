from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.api_routers.auth import get_current_user
from core.controllers import add_task_controller, get_user_tasks_controller, update_user_tasks_controller, \
     delete_user_task_controller
from core.middlewares.database_session import generate_session
from core.schemas import TaskModel, TaskUpdateModel
from core.store import UserTable
from core.models import tasks_get, get_task_by_id

tasks_router = APIRouter()


@tasks_router.post('/api/task')
def add_task(task: TaskModel, user: UserTable = Depends(get_current_user)):
    """ POST endpoint that adds task to database

    :param task: TaskModel
    :param user: User
    :return: Json
    """

    return add_task_controller(user, task)


@tasks_router.get('/api/tasks')
def get_tasks(session: Session = Depends(generate_session)):
    """ GET endpoint that gets all tasks from database

    :param session: Session
    :return: Json
    """

    return tasks_get(session=session)


@tasks_router.get('/api/task/{task_id}')
def get_task(task_id: int, session: Session = Depends(generate_session)):

    """ GET endpoint that gets concrete task using id

    :param task_id: int
    :param session: Session
    :return: Json
    """

    return get_task_by_id(task_id=task_id, session=session)


@tasks_router.delete('/api/task/{task_id}')
def delete_task(task_id: int, user: UserTable = Depends(get_current_user),
                session: Session = Depends(generate_session)):
    """ DELETE endpoint that deletes task from using task id

    :param task_id: int
    :param user: User
    :param session: Session
    :return: None
    """

    return delete_user_task_controller(user, task_id)


@tasks_router.get('/api/user_tasks')
def get_user_tasks(user: UserTable = Depends(get_current_user)):
    """ GET endpoint that gets user's tasks

    :param user: User
    :param session: Session
    :return: Json
    """

    return get_user_tasks_controller(user)


@tasks_router.put('/api/task/{task_id}')
def update_task(task_id: int, task_model: TaskUpdateModel,
                user: UserTable = Depends(get_current_user)):

    return update_user_tasks_controller(user, task_id, task_model)
