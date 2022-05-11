from sqlalchemy.orm import Session

from configs import ranks
from models.game.game_adding_rank_methods import add_ranks_list
from store import User, Task


def filter_task_by_rank(user: User, subject: str, session: Session):
    """ filters all tasks by user's rank

    :param user: User
    :param subject: str
    :param session: Session
    :return filtered_tasks: List[Task]
    """
    db_tasks = session.query(Task).filter_by(subject=subject).all()
    tasks_list = add_ranks_list(ranks=ranks)
    filtered_tasks = []
    for task in db_tasks:
        print(task.is_moderated)
        if tasks_list.index(task.rank) <= tasks_list.index(user.rank) and len(task.is_moderated) == 0:
            filtered_tasks.append(task)
    return filtered_tasks
