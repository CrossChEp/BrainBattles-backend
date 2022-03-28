from sqlalchemy.orm import Session

from schemas import TaskModel
from store import Task, User


def generate_new_task(task_model: TaskModel, user: User,
                      session: Session) -> None:
    """generates task from task model `TaskModel` and
    adds it to database

    :param task_model: TaskModel
    :param user: User
    :param session: Session
    """

    task = Task(**task_model.dict())
    user.tasks.append(task)
    session.add(task)
    session.commit()
