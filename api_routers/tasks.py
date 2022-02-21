from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api_routers.auth import get_current_user
from schemas import TaskModel
from store import get_session, User
from models import task_add, tasks_get, task_get, task_delete, user_tasks_get

tasks_router = APIRouter()


@tasks_router.post('/api/task')
def add_task(task: TaskModel, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return task_add(task=task, user=user, session=session)


@tasks_router.get('/api/tasks')
def get_tasks(session: Session = Depends(get_session)):
    return tasks_get(session=session)


@tasks_router.get('/api/task')
def get_task(task_id: int, session: Session = Depends(get_session)):
    return task_get(task_id=task_id, session=session)


@tasks_router.delete('/api/task')
def delete_task(task_id: int, user: User = Depends(get_current_user),
                session: Session = Depends(get_session)):
    return task_delete(task_id=task_id, user=user, session=session)


@tasks_router.get('/api/user_tasks')
def get_user_tasks(user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    return user_tasks_get(user=user, session=session)