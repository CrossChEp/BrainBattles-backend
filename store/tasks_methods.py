from sqlalchemy.orm import Session

from schemas import TaskModel
from store import Task


def task_add(task: TaskModel, session: Session):
    new_task = Task(
        name=task.task_name,
        subject=task.subject,
        content=task.content,
        right_answer=task.right_answer,

    )
    session.add(new_task)
    session.commit()