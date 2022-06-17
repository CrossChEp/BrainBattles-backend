from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.api_routers.auth import get_current_user
from core.controllers import add_task_controller
from core.middlewares.database_session import generate_session
from core.schemas import TaskModel, TaskUpdateModel
from core.store import UserTable
from core.models import task_add, tasks_get, task_get, task_delete, user_tasks_get, update_task_data

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


@tasks_router.get('/api/task')
def get_task(task_id: int, session: Session = Depends(generate_session)):

    """ GET endpoint that gets concrete task using id

    :param task_id: int
    :param session: Session
    :return: Json
    """

    return task_get(task_id=task_id, session=session)


@tasks_router.delete('/api/task')
def delete_task(task_id: int, user: UserTable = Depends(get_current_user),
                session: Session = Depends(generate_session)):
    """ DELETE endpoint that deletes task from using task id

    :param task_id: int
    :param user: User
    :param session: Session
    :return: None
    """

    return task_delete(task_id=task_id, user=user, session=session)


@tasks_router.get('/api/user_tasks')
def get_user_tasks(user: UserTable = Depends(get_current_user),
                   session: Session = Depends(generate_session)):
    """ GET endpoint that gets user's tasks

    :param user: User
    :param session: Session
    :return: Json
    """

    return user_tasks_get(user=user, session=session)


@tasks_router.put('/api/task')
def update_task(task_id: int, task_model: TaskUpdateModel,
                user: UserTable = Depends(get_current_user),
                session: Session = Depends(generate_session)):

    return update_task_data(
        task_id=task_id,
        task_model=task_model,
        user=user,
        session=session
    )
