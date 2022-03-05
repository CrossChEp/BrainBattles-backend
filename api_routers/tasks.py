from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_routers.auth import get_current_user
from schemas import TaskModel
from store import get_session, User
from models import task_add, tasks_get, task_get, task_delete, user_tasks_get

tasks_router = APIRouter()


@tasks_router.post('/api/task')
def add_task(task: TaskModel, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """ POST endpoint that adds task to database

    :param task: TaskModel
    :param user: User
    :param session: Session
    :return: Json
    """

    return task_add(task=task, user=user, session=session)


@tasks_router.get('/api/tasks')
def get_tasks(session: Session = Depends(get_session)):
    """ GET endpoint that gets all tasks from database

    :param session: Session
    :return: Json
    """

    return tasks_get(session=session)


@tasks_router.get('/api/task')
def get_task(task_id: int, session: Session = Depends(get_session)):

    """ GET endpoint that gets concrete task using id

    :param task_id: int
    :param session: Session
    :return: Json
    """

    return task_get(task_id=task_id, session=session)


@tasks_router.delete('/api/task')
def delete_task(task_id: int, user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    """ DELETE endpoint that deletes task from using task id

    :param task_id: int
    :param user: User
    :param session: Session
    :return: None
    """

    return task_delete(task_id=task_id, user=user, session=session)


@tasks_router.get('/api/user_tasks')
def get_user_tasks(user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    """ GET endpoint that gets user's tasks

    :param user: User
    :param session: Session
    :return: Json
    """

    return user_tasks_get(user=user, session=session)