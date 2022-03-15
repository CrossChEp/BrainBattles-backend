from sqlalchemy.orm import Session

from store import User, Task


def filter_task_by_rank(user: User, subject: str, session: Session):
    tasks = session.query(Task).filter_by(subject=subject).all()
    filtered_tasks = []
    for task in tasks:
        if task.rank <= user.rank:
            filtered_tasks.append(task)
    return filtered_tasks
