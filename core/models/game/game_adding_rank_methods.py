from core.configs.config import ranks
from core.store import UserTable


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


def filter_by_rank(users: list, active_user: UserTable):
    """
    filters tasks in queue regarding user's rank
    :param users: list
    :param active_user: User
    :return: list
    """
    ranks_list = add_ranks_list(ranks=ranks)
    available_ranks = []
    res = []
    for index, rank in enumerate(ranks_list):
        if rank == active_user.rank:
            available_ranks.append(ranks_list[index - 1])
            available_ranks.append(ranks_list[index])
            available_ranks.append(ranks_list[index + 1])

    for user in users:
        if user['rank'] in available_ranks and user['user_id'] != active_user.id:
           res.append(user)

    return res

