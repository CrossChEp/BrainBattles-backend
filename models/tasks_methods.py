from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas import TaskModel
from store import Task, User


def task_add(task: TaskModel, user: User, session: Session):
    new_task = Task(
        name=task.task_name,
        subject=task.subject,
        content=task.content,
        right_answer=task.right_answer,

    )
    user.tasks.append(new_task)
    session.add(new_task)
    session.commit()


def tasks_get(session: Session):
    return session.query(Task).all()


def task_get(task_id: int, session: Session):
    task = session.query(Task).filter_by(id=task_id).first()
    return task


def task_delete(task_id: int, user: User, session: Session):
    task = session.query(Task).filter_by(id=task_id).first()
    if task not in user.tasks:
        raise HTTPException(status_code=405)
    session.delete(task)
    session.commit()


def user_tasks_get(user: User, session: Session):
    return user.tasks
