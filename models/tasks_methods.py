import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas import TaskModel
from store import Task, User


def get_random_task(tasks: list):
    """
    gets random task regarding users' subject
    :param tasks: list
    :return: Task, bool
    """
    random_task_index = random.randint(0, len(tasks) - 1)
    try:
        random_task = tasks[random_task_index]
        return random_task
    except IndexError:
        return False


def task_add(task: TaskModel, user: User, session: Session):
    """
    adds task to database
    :param task: TaskModel
    :param user: User
    :param session: Session
    :return: None
    """
    new_task = Task(**task.dict())
    user.tasks.append(new_task)
    session.add(new_task)
    session.commit()


def tasks_get(session: Session):
    """
    gets all task from database
    :param session: Session
    :return: Query
    """
    return session.query(Task).all()


def task_get(task_id: int, session: Session):
    """
    gets concrete task using task id
    :param task_id: int
    :param session: Session
    :return: Task
    """
    task = session.query(Task).filter_by(id=task_id).first()
    return task


def task_delete(task_id: int, user: User, session: Session):
    """
    deletes task from database using task id
    :param task_id: int
    :param user: User
    :param session: Session
    :return: None
    """
    task = session.query(Task).filter_by(id=task_id).first()
    if task not in user.tasks:
        raise HTTPException(status_code=403, detail="You don't have such a permission")
    session.delete(task)
    session.commit()


def user_tasks_get(user: User, session: Session):
    """
    gets user's tasks
    :param user: User
    :param session: Session
    :return: Json
    """
    return user.tasks
