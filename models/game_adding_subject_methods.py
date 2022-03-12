from sqlalchemy.orm import Session

from models import delete_from_staging
from store import Staging, User, Game, Task
import random


def filtered_users(subject: str, queue: list):
    """
    filters users int queue regarding user's subject
    :param subject: int
    :param session: Session
    :return: list
    """
    res = []
    for user in queue:
        if user['subject'] == subject:
            res.append(user)
    return res


def get_random_user(users: list):
    """
    gets random user from queue
    :param users: list
    :return: bool, User
    """
    random_id = random.randint(0, len(users))
    try:
        random_user = users[random_id]
        return random_user
    except IndexError:
        return False


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


def database_task_adding(task: Task, user_id: int,
                         opponent_id: int, session: Session):
    """
    adds task to game database
    :param task: Task
    :param user_id: int
    :param opponent_id: int
    :param session: Session
    :return: None
    """
    user_game = session.query(Game).filter_by(user_id=user_id, opponent_id=opponent_id).first()
    opponent_game = session.query(Game).filter_by(user_id=opponent_id, opponent_id=user_id).first()
    task.games.append(user_game)
    task.games.append(opponent_game)
    session.commit()