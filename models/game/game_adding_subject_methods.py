def filtered_users(subject: str, queue: list):
    """
    filters users in queue regarding user's subject
    :param subject: int
    :param queue: List[QueueModel]
    :return: list
    """
    res = []
    for user in queue:
        if user['subject'] == subject:
            res.append(user)
    return res
