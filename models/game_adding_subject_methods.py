from sqlalchemy.orm import Session

from models import delete_from_staging
from store import Staging, User, Game, Task
import random


def filtered_users(subject: str, session: Session):
    queue = session.query(Staging).all()
    filtered = []
    for user in queue:
        if user.subject == subject:
            filtered.append(user)
    return filtered


def get_random_user(users: list):
    random_id = random.randint(0, len(users))
    try:
        random_user = users[random_id]
        return random_user
    except IndexError:
        return False


def get_random_task(tasks: list):
    random_task_index = random.randint(0, len(tasks) - 1)
    try:
        random_task = tasks[random_task_index]
        return random_task
    except IndexError:
        return False


def search_opponent(users: list, user: User):
    flag = False
    random_user = None
    if not users:
        return False
    while not flag:
        random_user = get_random_user(users=users)
        if random_user and random_user.user_id != user.id:
            flag = True
    return random_user


def database_users_adding(user: User, opponent: User, session: Session):
    user_opponent = Game(opponent_id=opponent.id)
    opponent_opponent = Game(opponent_id=user.id)
    session.add(user_opponent)
    user.game.append(user_opponent)
    session.add(opponent_opponent)
    opponent.game.append(opponent_opponent)
    session.commit()
    delete_from_staging(user=user, session=session)
    delete_from_staging(user=opponent, session=session)
    session.commit()


def database_task_adding(task: Task, user_id: int,
                         opponent_id: int, session: Session):
    user_game = session.query(Game).filter_by(user_id=user_id, opponent_id=opponent_id).first()
    opponent_game = session.query(Game).filter_by(user_id=opponent_id, opponent_id=user_id).first()
    task.games.append(user_game)
    task.games.append(opponent_game)
    session.commit()