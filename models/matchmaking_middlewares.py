from schemas import QueueModel
from store import User


def generate_queue_model(user: User, subject: str) -> QueueModel:
    user_json = QueueModel(
        user_id=user.id,
        subject=subject,
        rank=user.rank
    )
    return user_json


def search_subject(queue: list, user_id: int):
    subject = str()
    for user in queue:
        if user['user_id'] == user_id:
            subject = user['subject']
    return subject


def delete_user(queue: list, user_model: QueueModel):
    for user_index, user in enumerate(queue):
        if user_model == user:
            queue.pop(user_index)
    return queue
