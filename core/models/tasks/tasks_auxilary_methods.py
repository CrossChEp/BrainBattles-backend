from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session, Query

from core.configs.config import NOT_MODERATED
from core.models.user.user_methods import get_user_by_id
from core.schemas import TaskAddModel, TaskGetModel
from core.store import TaskTable, UserTable


def generate_new_task(task_model: TaskAddModel, user: UserTable,
                      session: Session) -> None:
    """generates task from task model `TaskModel` and
    adds it to database

    :param task_model: TaskModel
    :param user: User
    :param session: Session
    """
    user = get_user_by_id(user.id, session)
    task = TaskTable(**task_model.dict())
    task.state = NOT_MODERATED
    user.tasks.append(task)
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
        raise HTTPException(status_code=404, detail='No users were found')


def is_user_allowed_to_change_task(user: UserTable, task: Query):
    """checks if user allowed to change the task

    :param user: User
        (current user)
    :param task: Query
        (query of task)
    """
    if task.one() not in user.tasks:
        raise HTTPException(status_code=403, detail="You don't have permission to update this task")


def create_task_get_model(task: TaskTable) -> TaskGetModel:
    task_model = TaskGetModel(
        id=task.id,
        name=task.name,
        subject=task.subject,
        content=task.content,
        rank=task.rank,
        state=task.state
    )
    return task_model


def create_list_of_task_models(task_list: list) -> List[TaskGetModel]:
    list_of_task_get_models = []
    for task in task_list:
        task_get_model = create_task_get_model(task)
        list_of_task_get_models.append(task_get_model)
    return list_of_task_get_models
