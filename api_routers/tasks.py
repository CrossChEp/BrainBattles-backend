from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import TaskModel
from store import get_session, task_add

tasks_router = APIRouter()


@tasks_router.post('/api/task')
def add_task(task: TaskModel, session: Session = Depends(get_session)):
    return task_add(task=task, session=session)