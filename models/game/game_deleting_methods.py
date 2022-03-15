from schemas.api_models import GameModel


def delete_from_game(user_model: GameModel, game: list):
    if user_model.dict() not in game:
        return False
    game.pop(game.index(user_model.dict()))
    return game
