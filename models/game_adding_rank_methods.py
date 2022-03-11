from configs.config import ranks
from store import User


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


def filter_by_rank(users: list, user: User):
    """
    filters users in queue regarding user's rank
    :param users: list
    :param user: User
    :return: list
    """
    ranks_list = add_ranks_list(ranks=ranks)
    res = []
    for user_stage in users:
        for rank in range(len(ranks_list)):
            if ranks_list[rank] == user.rank:
                try:
                    if user_stage.user_id != user.id and (user_stage.rank == ranks_list[rank]
                            or user_stage.rank == ranks_list[-1]
                            or user_stage.rank == ranks_list[+1]):
                        res.append(user_stage)
                except IndexError:
                    pass
    return res