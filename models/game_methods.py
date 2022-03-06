import random

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from configs import ranks
from models import delete_from_staging
from store import User, Staging, Game, Task


def add_ranks_list(ranks: dict) -> list:
    """
    creates list from ranks' dict
    :param ranks: dict
    :return: list
    """
    ranks_list = []
    for key, value in ranks.items():
        ranks_list.append(value)
    return ranks_list


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


def add_to_game(user: User, session: Session):
    """
    adds user to game
    :param user: User
    :param session: Session
    :return: dict
    """
    user_staging = session.query(Staging).filter_by(user_id=user.id).first()
    if not user_staging:
        raise HTTPException(status_code=403, detail='User not in queue')
    users_filtered = filtered_users(subject=user_staging.subject, session=session)
    random_user = search_opponent(users=users_filtered, user=user)
    opponent = session.query(User).filter_by(id=random_user.user_id).first()
    tasks = session.query(Task).filter_by(subject=user_staging.subject).all()
    random_task = get_random_task(tasks=tasks)
    if not random_task:
        raise HTTPException(status_code=404, detail='No task with such subject')
    database_users_adding(user=user, opponent=opponent, session=session)
    database_task_adding(task=random_task, user_id=user.id,
                         opponent_id=opponent.id, session=session)
    return {'task': random_task.id}


def leave_game(user: User, session: Session):
    """
    deletes user from game
    :param user: User
    :param session: Session
    :return: None
    """
    session_user = session.query(Game).filter_by(user_id=user.id).first()
    session_user_opponent = session.query(Game).filter_by(opponent_id=user.id).first()
    if session_user is None or session_user_opponent is None:
        raise HTTPException(status_code=403, detail='User is not in the game')
    session.delete(session_user)
    session.delete(session_user_opponent)
    session.commit()


def make_try(answer: str, user: User, session: Session):
    """
    makes try
    :param answer: str
    :param user: User
    :param session: Session
    :return: None
    """
    game_checking = session.query(Game).filter_by(user_id=user.id).first()
    if not game_checking:
        raise HTTPException(status_code=403, detail='User is not in game')
    task = session.query(Task).filter_by(id=game_checking.task).first()
    if task.right_answer == answer:
        leave_game(user=user, session=session)
        user.scores += task.scores
        scores = list(ranks.keys())
        for index, score in enumerate(scores):
            try:
                if user.scores < scores[index + 1]:
                    new_rank = ranks[score]
                    user.rank = new_rank
                    break
            except IndexError:
                pass
        session.commit()
        return
    raise HTTPException(status_code=400, detail='Wrong answer')
