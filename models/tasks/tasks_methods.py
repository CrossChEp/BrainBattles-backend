import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from configs import ranks
from models.game.game_adding_rank_methods import add_ranks_list
from models.general_methods import model_without_nones
from models.tasks import generate_new_task
from schemas import TaskModel, TaskUpdateModel
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


def update_task_data(task_id: int, task_model: TaskUpdateModel,
                       session: Session, user: User) -> None:
    task = session.query(Task).filter_by(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail='No tasks were found')
    if task not in user.tasks:
        raise HTTPException(status_code=403, detail="You don't have permission to update this task")

    clear_task_model = model_without_nones(model=task_model.dict())
    task.update(**clear_task_model)
    session.commit()

