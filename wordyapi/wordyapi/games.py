import uuid

import wordylib.game


_GAMES_DATA = {}


def create_game() -> str:
    game = wordylib.game.Game()
    game_id = str(uuid.uuid4())
    _GAMES_DATA[game_id] = {"game": game, "players": {}}
    return game_id


def get_game(game_id: str) -> wordylib.game.Game:
    return _GAMES_DATA[game_id]["game"]


def create_player(game_id: str, player_name: str) -> str:
    game = get_game(game_id=game_id)
    game.add_player(player=player_name)
    player_id = str(uuid.uuid4())
    _GAMES_DATA[game_id]["players"][player_id] = player_name
    return player_id


def get_player(game_id: str, player_id: str) -> str:
    return _GAMES_DATA[game_id]["players"][player_id]
