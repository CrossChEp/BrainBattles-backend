from sqlalchemy.orm import Session

from configs import ranks
from models.game.game_adding_rank_methods import add_ranks_list
from store import User, Task


def filter_task_by_rank(user: User, subject: str, session: Session):
    db_tasks = session.query(Task).filter_by(subject=subject).all()
    tasks_list = add_ranks_list(ranks=ranks)
    filtered_tasks = []
    for task in db_tasks:
        if tasks_list.index(task.rank) <= tasks_list.index(user.rank):
            filtered_tasks.append(task)
    return filtered_tasks