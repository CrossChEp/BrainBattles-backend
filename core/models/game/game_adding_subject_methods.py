def filtered_users(subjects: list, queue: list):
    """
    filters users in queue regarding user's subject
    :param subjects: list
    :param queue: List[QueueModel]
    :return: list
    """
    opponents = []
    for user in queue:
        if does_opponent_has_same_subjects(subjects, user['subjects']):
            opponents.append(user)
    return opponents


def does_opponent_has_same_subjects(user_subjects: list, opponent_subjects: list) -> bool:
    """checks if opponent has the same subject as user

    :param user_subjects: list
        (subjects that user chose)
    :param opponent_subjects: list
        (subjects that opponent chose)
    :return: bool
    """
    for subject in user_subjects:
        if subject in opponent_subjects:
            return True
    return False


def get_game_subject(user_subjects: list, opponent_subjects: list) -> str:
    """gets the first subject that user and opponent have

    :param user_subjects: list
        (subjects that user chose)
    :param opponent_subjects: list
        (subjects that opponent chose)
    :return: str
    """
    game_subject = None
    for subject in user_subjects:
        if subject in opponent_subjects:
            game_subject = subject
    return game_subject
