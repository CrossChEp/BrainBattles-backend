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