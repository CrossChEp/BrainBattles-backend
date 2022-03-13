from sqlalchemy.orm import Session
from store import Game, Task


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