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
