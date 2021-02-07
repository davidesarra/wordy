import random

import pytest

from wordylib import errors
from wordylib.game import Game


@pytest.fixture
def two_round_game():
    random.seed(100)
    player1 = "Davide"
    player2 = "Cherry"

    game = Game()
    game.add_player(player=player1)
    game.add_player(player=player2)
    game.draw()
    game.submit(
        player=player2,
        solution=[["A", "r", "I", "A"], [" ", "I", " ", " "], [" ", "M", "U", "D"]],
    )
    game.draw()
    game.submit(player=player2, solution=[["S", "O"]])
    return game


def test_game_add_player():
    # given
    player = "Davide"
    expected = {player}

    # when
    game = Game()
    game.add_player(player=player)
    result = game.players

    # then
    assert result == expected


def test_game_add_player_multiple_times():
    # given
    player1 = "Davide"
    player2 = "Cherry"
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
    player = "Davide"

    # when and then
    game = Game()
    game.add_player(player=player)
    expected_msg = "^Davide is already playing$"
    with pytest.raises(ValueError, match=expected_msg):
        game.add_player(player=player)


def test_game_draw_with_no_players():
    # given
    expected_msg = "^Cannot draw because there are no players$"

    # when and then
    game = Game()
    with pytest.raises(errors.WordylibError, match=expected_msg):
        game.draw()


def test_game_draw():
    # given
    random.seed(100)

    # when
    game = Game()
    game.add_player(player="Davide")
    result = game.draw()

    # then
    expected = {
        "D": {"count": 1, "points": 1},
        "I": {"count": 3, "points": 1},
        "S": {"count": 2, "points": 1},
        "R": {"count": 2, "points": 1},
        "M": {"count": 1, "points": 1},
        "A": {"count": 2, "points": 1},
        "U": {"count": 1, "points": 1},
    }
    assert result == expected


def test_game_current_draw():
    # given
    random.seed(100)

    # when
    game = Game()
    game.add_player(player="Davide")
    game.draw()
    result = game.current_draw

    # then
    expected = {
        "D": {"count": 1, "points": 1},
        "I": {"count": 3, "points": 1},
        "S": {"count": 2, "points": 1},
        "R": {"count": 2, "points": 1},
        "M": {"count": 1, "points": 1},
        "A": {"count": 2, "points": 1},
        "U": {"count": 1, "points": 1},
    }
    assert result == expected


def test_game_current_draw_before_starting_playing():
    # given

    # when and then
    game = Game()
    expected_msg = "^Game has not started yet, draw first$"
    with pytest.raises(errors.WordylibError, match=expected_msg):
        game.current_draw


def test_game_current_round_before_starting_playing():
    # given

    # when and then
    game = Game()
    expected_msg = "^Game has not started yet, draw first$"
    with pytest.raises(errors.WordylibError, match=expected_msg):
        game.current_round


def test_game_current_round_after_playing_a_round():
    # given
    expected = 1

    # when
    game = Game()
    game.add_player(player="Davide")
    game.draw()
    result = game.current_round

    # then
    assert result == expected


def test_game_submit_solution_without_anyone_playing():
    # given
    player = "Davide"
    solution = [[]]

    # when and then
    game = Game()
    game.add_player(player=player)
    expected_msg = "^Game has not started yet, draw first$"
    with pytest.raises(errors.WordylibError, match=expected_msg):
        game.submit(player=player, solution=solution)


def test_game_submit_solution_and_get_word_scores_for_round(two_round_game):
    # when
    result = two_round_game.get_word_scores(round=1)

    # then
    expected = {"Cherry": {"ARIA": 4, "RIM": 3, "MUD": 3}, "Davide": {}}
    assert result == expected


def test_game_submit_solution_and_get_total_scores_for_round(two_round_game):
    # when
    result = two_round_game.get_total_scores(round=1)

    # then
    expected = {"Cherry": 10, "Davide": 0}
    assert result == expected


def test_game_submit_solution_and_get_word_scores_for_entire_game(two_round_game):
    # when
    result = two_round_game.get_word_scores()

    # then
    expected = {"Cherry": {"ARIA": 4, "RIM": 3, "MUD": 3, "SO": 2}, "Davide": {}}
    assert result == expected


def test_game_submit_solution_and_get_total_scores_for_entire_game(two_round_game):
    # when
    result = two_round_game.get_total_scores()

    # then
    expected = {"Cherry": 12, "Davide": 0}
    assert result == expected


def test_game_get_word_scores_for_unplayed_round(two_round_game):
    # given
    round = 3

    # when and then
    expected_msg = f"^Round {round} has not been played yet$"
    with pytest.raises(ValueError, match=expected_msg):
        two_round_game.get_word_scores(round=round)


def test_game_get_word_scores_before_adding_any_player():
    # when
    game = Game()
    result = game.get_word_scores()

    # then
    expected = {}
    assert result == expected


def test_game_get_total_scores_before_adding_any_player():
    # when
    game = Game()
    result = game.get_total_scores()

    # then
    expected = {}
    assert result == expected


def test_game_get_total_scores_before_playing_any_round():
    # given
    player = "Davide"

    # when
    game = Game()
    game.add_player(player=player)
    result = game.get_total_scores()

    # then
    expected = {"Davide": 0}
    assert result == expected


@pytest.mark.parametrize(
    "solution",
    (
        [["M", "A", "D"], ["U", " ", " "], ["D", " ", " "]],
        [["M", "A", "T"], ["U", " ", " "], ["D", " ", " "]],
    ),
)
def test_game_submit_solution_overusing_drawn_letters(solution):
    # given
    random.seed(100)
    player = "Davide"

    # when and then
    game = Game()
    game.add_player(player=player)
    game.draw()
    expected_msg = r"^Some letters were used too many times \(.*\)$"
    with pytest.raises(errors.InvalidSubmission, match=expected_msg):
        game.submit(player=player, solution=solution)


def test_game_submit_solution_reusing_previous_words(two_round_game):
    # given
    solution = [["S", "O"]]

    # when and then
    two_round_game.draw()
    expected_msg = r"^Some words were already used \(SO\)$"
    with pytest.raises(errors.InvalidSubmission, match=expected_msg):
        two_round_game.submit(player="Cherry", solution=solution)
    two_round_game.submit(player="Davide", solution=solution)
