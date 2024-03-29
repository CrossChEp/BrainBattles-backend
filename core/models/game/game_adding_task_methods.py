from sqlalchemy.orm import Session

from core.configs import ranks
from core.models.game.game_adding_rank_methods import add_ranks_list
from core.store import UserTable, TaskTable


def filter_task_by_rank(user: UserTable, subject: str, session: Session):
    """ filters all users by user's rank

    :param user: User
    :param subject: str
    :param session: Session
    :return filtered_tasks: List[Task]
    """
    db_tasks = session.query(TaskTable).filter_by(subject=subject).all()
    tasks_list = add_ranks_list(ranks=ranks)
    filtered_tasks = []
    for task in db_tasks:
        print(task.is_moderated)
        if tasks_list.index(task.rank) <= tasks_list.index(user.rank) and len(task.is_moderated) == 0:
            filtered_tasks.append(task)
    return filtered_tasks
