from core.schemas import QueueModel
from core.store import UserTable


def generate_queue_model(user: UserTable, subjects: list) -> QueueModel:
    """ generates QueueModule using User(user's database cell)
        and subject
    :param user: User
    :param subjects: list
    :return user_json: QueueModel

    """
    user_json = QueueModel(
        user_id=user.id,
        subjects=subjects,
        rank=user.rank
    )
    return user_json


def search_subjects(queue: list, user_id: int) -> list:
    """ finds subjects from
        user's queue place
    :param queue: list
    :param user_id: int
    :return subject: str
    """
    subjects = []
    for user in queue:
        if user['user_id'] == user_id:
            subjects = user['subjects']
    return subjects


def delete_user(queue: list, user_model: QueueModel):
    """ deletes user
        from queue(redis)
    :param queue: list
    :param user_model: QueueModel
    :return queue: list

    """
    for user_index, user in enumerate(queue):
        if user_model == user:
            queue.pop(user_index)
    return queue
