import pytest

from wordy.game import Game
from wordy.game_interface import GameInterface


def test_game_to_run_n_rounds(mocker):
    player_names = ["Jim", "Tom T. Jones"]
    n_rounds = 2
    round_duration = 60

    mocker.patch.object(GameInterface, "get_players_names", return_value=player_names)
    mocker.patch.object(GameInterface, "get_n_rounds", return_value=n_rounds)
    mocker.patch.object(GameInterface, "get_round_time", return_value=round_duration)
    mocker.patch.object(GameInterface, "get_language", return_value="en")
    mocker.patch.object(GameInterface, "get_if_ready_for_next_round", return_value="")
    mocker.patch.object(GameInterface, "show_new_round")
    mocker.patch.object(GameInterface, "show_letter_draw")
    mocker.patch.object(GameInterface, "show_round_timer")
    mocker.patch.object(GameInterface, "get_solutions")
    mocker.patch.object(GameInterface, "show_scores_by_word_and_player")
    mocker.patch.object(GameInterface, "show_round_scores")
    mocker.patch.object(GameInterface, "show_running_scores")
    mocker.patch.object(GameInterface, "show_final_scores")

    game = Game()
    game.play_game()

    GameInterface.get_players_names.assert_called_once()
    GameInterface.get_n_rounds.assert_called_once()
    GameInterface.get_language.assert_called_once()
    assert GameInterface.get_if_ready_for_next_round.call_count == n_rounds
    assert GameInterface.show_new_round.call_count == n_rounds
    assert GameInterface.show_letter_draw.call_count == n_rounds
    assert GameInterface.show_round_timer.call_count == n_rounds
    GameInterface.show_round_timer.assert_called_with(seconds=round_duration)
    assert GameInterface.get_solutions.call_count == n_rounds
    GameInterface.get_solutions.assert_called_with(player_names=player_names)
    assert GameInterface.show_scores_by_word_and_player.call_count == n_rounds
    GameInterface.show_running_scores.assert_called_once()
    GameInterface.show_final_scores.assert_called_once()
    GameInterface.show_final_scores.assert_called_with(
        scores={player_name: 0 for player_name in player_names}
    )


def test_game_to_run_until_halted(mocker):
    player_names = ["Jim"]
    n_rounds = None
    play_new_round = [True, False]
    round_duration = 60
    true_n_rounds = 1 + sum(play_new_round)

    mocker.patch.object(GameInterface, "get_players_names", return_value=player_names)
    mocker.patch.object(GameInterface, "get_n_rounds", return_value=n_rounds)
    mocker.patch.object(GameInterface, "get_round_time", return_value=round_duration)
    mocker.patch.object(GameInterface, "get_language", return_value="en")
    mocker.patch.object(
        GameInterface, "get_whether_play_new_round", side_effect=play_new_round
    )
    mocker.patch.object(GameInterface, "get_if_ready_for_next_round", return_value="")
    mocker.patch.object(GameInterface, "show_new_round")
    mocker.patch.object(GameInterface, "show_letter_draw")
    mocker.patch.object(GameInterface, "show_round_timer")
    mocker.patch.object(GameInterface, "get_solutions")
    mocker.patch.object(GameInterface, "show_scores_by_word_and_player")
    mocker.patch.object(GameInterface, "show_round_scores")
    mocker.patch.object(GameInterface, "show_running_scores")
    mocker.patch.object(GameInterface, "show_final_scores")

    game = Game()
    game.play_game()

    assert GameInterface.get_whether_play_new_round.call_count == len(play_new_round)
    GameInterface.get_players_names.assert_called_once()
    GameInterface.get_n_rounds.assert_called_once()
    GameInterface.get_language.assert_called_once()
    assert GameInterface.get_if_ready_for_next_round.call_count == true_n_rounds
    assert GameInterface.show_new_round.call_count == true_n_rounds
    assert GameInterface.show_letter_draw.call_count == true_n_rounds
    assert GameInterface.show_round_timer.call_count == true_n_rounds
    GameInterface.show_round_timer.assert_called_with(seconds=round_duration)
    assert GameInterface.get_solutions.call_count == true_n_rounds
    GameInterface.get_solutions.assert_called_with(player_names=player_names)
    assert GameInterface.show_scores_by_word_and_player.call_count == true_n_rounds
    GameInterface.show_running_scores.assert_called_once()
    GameInterface.show_final_scores.assert_called_once()
    GameInterface.show_final_scores.assert_called_with(
        scores={player_name: 0 for player_name in player_names}
    )
