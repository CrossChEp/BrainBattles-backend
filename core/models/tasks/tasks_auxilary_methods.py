from fastapi import HTTPException
from sqlalchemy.orm import Session, Query

from core.schemas import TaskModel
from core.store import TaskTable, UserTable, TaskModerationTable


def generate_new_task(task_model: TaskModel, user: UserTable,
                      session: Session) -> None:
    """generates task from task model `TaskModel` and
    adds it to database

    :param task_model: TaskModel
    :param user: User
    :param session: Session
    """

    task = TaskTable(**task_model.dict())
    user.tasks.append(task)
    moderated_task = TaskModerationTable()
    task.is_moderated.append(moderated_task)
    session.add(task)
    session.commit()


def check_task_availability(user: UserTable, task: Query):
    """checks if user can change the task

    :param user: User
        (current user)
    :param task: Query
        (query of task)
    """
    is_task_exists(task=task)
    is_user_allowed_to_change_task(user=user, task=task)


def is_task_exists(task: Query):
    """ checks if task exists in database
    :param task: Query
        (query of task)
    """
    if not task.one():
        raise HTTPException(status_code=404, detail='No tasks were found')


def is_user_allowed_to_change_task(user: UserTable, task: Query):
    """checks if user allowed to change the task

    :param user: User
        (current user)
    :param task: Query
        (query of task)
    """
    if task.one() not in user.tasks:
        raise HTTPException(status_code=403, detail="You don't have permission to update this task")
