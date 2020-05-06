import pytest

from wordylib.game import Game


def test_game_add_player():
    # given
    player = "davide"
    expected = {player}

    # when
    game = Game()
    game.add_player(player=player)
    result = game.players

    # then
    assert result == expected


def test_game_add_player_multiple_times():
    # given
    player1 = "davide"
    player2 = "cherry"
    expected = {player1, player2}

    # when
    game = Game()
    game.add_player(player=player1)
    game.add_player(player=player2)
    result = game.players

    # then
    assert result == expected


def test_game_add_player_same_player_twice():
    # given
    player = "davide"

    # when and then
    game = Game()
    game.add_player(player=player)
    with pytest.raises(ValueError, match="^davide is already playing$"):
        game.add_player(player=player)
