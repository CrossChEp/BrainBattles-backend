from schemas import QueueModel
from store import User


def generate_queue_model(user: User, subject: str) -> QueueModel:
    """ generates QueueModule using User(user's database cell)
        and subject
    :param user: User
    :param subject: str
    :return user_json: QueueModel

    """
    user_json = QueueModel(
        user_id=user.id,
        subject=subject,
        rank=user.rank
    )
    return user_json


def search_subject(queue: list, user_id: int):
    """ finds subject from
        user's queue place
    :param queue: list
    :param user_id: int
    :return subject: str
    """
    subject = str()
    for user in queue:
        if user['user_id'] == user_id:
            subject = user['subject']
    return subject


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
