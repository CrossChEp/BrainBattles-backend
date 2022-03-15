from schemas.api_models import GameModel


def delete_from_game(user_model: GameModel, game: list):
    """ deletes user from game
    :param user_model: GameModel
    :param game: List[GameModel]
    :return game: List[GameModel]

    """
    if user_model.dict() not in game:
        return False
    game.pop(game.index(user_model.dict()))
    return game
