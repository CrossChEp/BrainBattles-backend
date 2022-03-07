from fastapi import HTTPException
from sqlalchemy.orm import Session

from configs import ranks
from models.game_adding_subject_methods import filtered_users, search_opponent, get_random_task, database_users_adding, \
    database_task_adding
from store import User, Staging, Game, Task
from models.game_adding_rank_methods import filter_by_rank


def user_adding(user_staging, user: User, session: Session):
    """
    adds user to database
    :param user_staging:
    :param user: User
    :param session: Session
    :return: int
    """

    while True:
        users_filtered_by_subject = filtered_users(subject=user_staging.subject, session=session)
        users_filtered = filter_by_rank(users=users_filtered_by_subject, user=user)
        if not users_filtered:
            continue
        random_user = search_opponent(users=users_filtered, user=user)
        opponent = session.query(User).filter_by(id=random_user.user_id).first()
        tasks = session.query(Task).filter_by(subject=user_staging.subject).all()
        random_task = get_random_task(tasks=tasks)
        if not random_task:
            raise HTTPException(status_code=404, detail='No task with such subject')
        database_users_adding(user=user, opponent=opponent, session=session)
        database_task_adding(task=random_task, user_id=user.id,
                             opponent_id=opponent.id, session=session)
        return random_task.id


def add_to_game(user: User, session: Session):
    """
    adds user to game
    :param user: User
    :param session: Session
    :return: dict
    """

    game = session.query(Game).filter_by(user_id=user.id).first()
    if game:
        return {'task': game.task}
    user_staging = session.query(Staging).filter_by(user_id=user.id).first()
    if not user_staging:
        raise HTTPException(status_code=403, detail='User not in queue')
    adding = user_adding(user_staging=user_staging, user=user, session=session)
    return {'task': adding}


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
