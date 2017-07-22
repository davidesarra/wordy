from wordy.errors import (
    InvalidSubmission,
    InvalidWord,
)
from wordy.game_interface import GameInterface
from wordy.scoreboard import Scoreboard


class Game:
    def __init__(self) -> None:
        self._interface = GameInterface()
        self._interface.show_game_intro()
        self._scoreboard = Scoreboard(
            players=self._interface.get_players_names(),
            language=self._interface.get_language(),
        )
        self._n_rounds = self._interface.get_n_rounds()
        self._is_unbounded_game = not bool(self._n_rounds)
        self._round_time = self._interface.get_round_time()

    def play_game(self) -> None:
        while (
            self._is_unbounded_game or self._scoreboard.current_round < self._n_rounds
        ):
            self._interface.get_if_ready_for_next_round()
            self._play_round()
            if self._is_unbounded_game:
                play_new_round = self._interface.get_whether_play_new_round(
                    played_rounds=self._scoreboard.current_round
                )
                if not play_new_round:
                    break
            if self._scoreboard.current_round != self._n_rounds:
                self._interface.show_running_scores(
                    scores=self._scoreboard.get_total_scores()
                )
        self._interface.show_final_scores(scores=self._scoreboard.get_total_scores())

    def _play_round(self) -> None:
        self._scoreboard.start_round()
        self._interface.show_new_round(round_number=self._scoreboard.current_round)
        self._interface.show_letter_draw(
            letter_draw=self._scoreboard.current_letter_draw
        )
        self._interface.show_round_timer(seconds=self._round_time)
        self._score_round()
        self._interface.show_scores_by_word_and_player(
            scores=self._scoreboard.get_current_round_word_scores()
        )
        self._interface.show_round_scores(
            scores=self._scoreboard.get_current_round_total_scores()
        )

    def _score_round(self) -> None:
        solutions_by_player = self._interface.get_solutions(
            player_names=self._scoreboard.players
        )

        for player in self._scoreboard.players:
            solution = solutions_by_player[player]
            try:
                self._scoreboard.score(player=player, solution=solution)
            except (InvalidSubmission, InvalidWord) as error:
                self._interface.show_error(player=player, error=error)
