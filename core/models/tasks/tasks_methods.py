import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.configs import ranks
from core.models.user.user_methods import get_user_by_id
from core.models.game.game_adding_rank_methods import add_ranks_list
from core.models.general_methods import model_without_nones
from core.models.tasks import generate_new_task, check_task_availability
from core.schemas import TaskModel, TaskUpdateModel
from core.store import TaskTable, UserTable


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


def task_add(task: TaskModel, user: UserTable, session: Session):
    """
    adds task to database
    :param task: TaskModel
    :param user: User
    :param session: Session
    :return: None
    """
    rank_list = add_ranks_list(ranks)
    if task.rank not in rank_list:
        raise HTTPException(status_code=400, detail='Wrong rank')

    generate_new_task(task_model=task, session=session, user=user)


def tasks_get(session: Session):
    """
    gets all task from database
    :param session: Session
    :return: Query
    """
    return session.query(TaskTable).all()


def task_get(task_id: int, session: Session):
    """
    gets concrete task using task id
    :param task_id: int
    :param session: Session
    :return: Task
    """
    task = session.query(TaskTable).filter_by(id=task_id).first()
    return task


def task_delete(task_id: int, user: UserTable, session: Session):
    """
    deletes task from database using task id
    :param task_id: int
    :param user: User
    :param session: Session
    :return: None
    """
    task = session.query(TaskTable).filter_by(id=task_id).first()
    if task not in user.tasks:
        raise HTTPException(status_code=403, detail="You don't have such a permission")
    session.delete(task)
    session.commit()


def user_tasks_get(user: UserTable):
    """
    gets user's tasks
    :param user: User
    :param session: Session
    :return: Json
    """
    return user.tasks


def update_task_data(task_id: int, task_model: TaskUpdateModel,
                     session: Session, user: UserTable) -> None:
    """ updates user's task using task's id

    :param task_id: int
        (task's id)
    :param task_model: TaskUpdateModel
        (new task's data)
    :param session: Session
    :param user: User
        (current user)
    :return: None
    """

    task = session.query(TaskTable).filter_by(id=task_id)
    user = get_user_by_id(user.id, session)
    check_task_availability(user=user, task=task)

    clear_task_model = model_without_nones(model=task_model.dict())
    task.update(clear_task_model)
    session.commit()

