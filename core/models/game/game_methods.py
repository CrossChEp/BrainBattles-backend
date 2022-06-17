"""Module for adding user to game"""


import json

import redis
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.configs import ranks, QUEUE, GAME, redis
from core.middlewares import get_redis_table
from core.models import task_get
from core.models.game.game_adding_rank_methods import filter_by_rank
from core.models.game.game_adding_subject_methods import filtered_users, get_game_subject
from core.models.game.game_adding_task_methods import filter_task_by_rank
from core.models.game.game_auxiliary_methods import check_user_in_game, \
    get_random_user, adding_user_to_game, find_game, generate_game_model, check_user_in_queue, winner_exists, \
    set_winner, set_user_rank
from core.models.game.game_deleting_methods import delete_from_game
from core.models.matchmaking.matchmaking_auxilary_methods import search_subjects
from core.models.tasks.tasks_methods import get_random_task
from core.store import UserTable, TaskTable


def user_adding(user: UserTable, queue: list,
                subjects: list, session: Session):
    """
    adds user to database
    :param user: User
    :param queue: list
    :param subjects: list
    :param session: Session
    :return: dict
    """
    get_redis_table(GAME)
    get_redis_table(QUEUE)
    while True:
        game = get_redis_table(GAME)
        general_queue = get_redis_table(QUEUE)
        checking = check_user_in_game(user=user, games=game)
        checking_queue = check_user_in_queue(user, general_queue)
        if checking:
            return checking
        if not checking_queue:
            raise HTTPException(status_code=403, detail='User not in queue')
        opponents = filtered_users(subjects=subjects, queue=queue)
        opponents = filter_by_rank(users=opponents, active_user=user)
        if not opponents:
            continue
        opponent = get_random_user(users=opponents)
        if not opponent:
            continue
        subject = get_game_subject(user_subjects=subjects, opponent_subjects=opponent['subjects'])
        tasks = filter_task_by_rank(user=user, subject=subject, session=session)
        if not tasks:
            raise HTTPException(status_code=404, detail='No task with such subject')
        random_task = get_random_task(tasks)
        if not random_task:
            raise HTTPException(status_code=404, detail='No task with such subject')
        task = adding_user_to_game(user=user, opponent=opponent, random_task=random_task)
        return task


def add_to_game(user: UserTable, session: Session):
    """
    adds user to game
    :param user: User
    :param session: Session
    :return: dict
    """
    get_redis_table(table_name=QUEUE)
    queue = json.loads(redis.get(QUEUE))
    subjects = search_subjects(queue=queue, user_id=user.id)
    if not subjects:
        raise HTTPException(status_code=403, detail='User not in queue')
    task = user_adding(user=user, queue=queue, subjects=subjects, session=session)
    return task


def leave_game(user: UserTable, session: Session):
    """
    deletes user from game
    :param user: User
    :param session: Session
    :return: None
    """
    game = get_redis_table(GAME)
    user_game = find_game(user=user, games=game)
    if not user_game:
        raise HTTPException(status_code=403, detail='User not in game')
    task = task_get(task_id=user_game['task'], session=session)
    user_model = generate_game_model(user_id=user.id,
                                     opponent_id=user_game['opponent_id'], task=task)
    game = delete_from_game(user_model=user_model, game=game)
    redis.set(GAME, json.dumps(game))


def make_try(answer: str, user: UserTable, session: Session):
    """
    makes try
    :param answer: str
    :param user: User
    :param session: Session
    :return: None
    """
    games = get_redis_table(GAME)
    game_checking = find_game(user=user, games=games)
    if not game_checking:
        raise HTTPException(status_code=403, detail='User is not in game')
    task = session.query(TaskTable).filter_by(id=game_checking['task']).first()
    if task.right_answer == answer:
        if not winner_exists(game=game_checking):
            set_winner(game=game_checking, user=user, session=session)
            successful_try(user=user, task=task, session=session)
            return
        if winner_exists(game_checking) and game_checking['winner'] != user.id:
            leave_game(user=user, session=session)
            raise HTTPException(status_code=403, detail='You lost')
    raise HTTPException(status_code=400, detail='Wrong answer')


def successful_try(user: UserTable, task: TaskTable, session: Session):
    """ deletes user from game and gives
        scores to user. User only when user
        gave right answer!
        :param user: User
            current user
        :param task: Task
            task for which answer was given
        :param session: Session

    """
    leave_game(user=user, session=session)
    user.wins += 1
    user.scores += task.scores
    scores = list(ranks.keys())
    set_user_rank(scores=scores, user=user)
    session.commit()
