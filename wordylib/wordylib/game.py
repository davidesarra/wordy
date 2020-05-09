from typing import Any, Dict, List, Optional, Set

from wordylib import errors
from wordylib.alphabet import Alphabet
from wordylib.submission import Submission
from wordylib.validators import FromLettersValidator, NewWordValidator


class Game:
    _LANGUAGE_CODE = "en"
    _NUM_LETTERS_IN_DRAW = 12

    def __init__(self):
        self._players: Set[str] = set()
        self._alphabet = Alphabet.from_data(language_code=self._LANGUAGE_CODE)
        self._rounds = {}
        self._current_draw: Dict[str, Dict[str, int]]

    @property
    def players(self) -> Set[str]:
        return {*self._players}

    def add_player(self, player: str) -> None:
        if player in self._players:
            raise ValueError(f"{player} is already playing")
        self._players.add(player)

    @property
    def current_round(self):
        self._raise_if_the_game_has_not_started_yet()
        return len(self._rounds)

    def draw(self) -> Dict[str, Dict[str, int]]:
        """Draw letters and start new round."""
        if not self._players:
            raise errors.WordylibError("Cannot draw because there are no players")

        draw = self._alphabet.draw(num_letters=self._NUM_LETTERS_IN_DRAW)
        round = len(self._rounds) + 1

        self._current_draw, self._rounds[round] = draw, {}

        return draw

    def submit(self, player: str, solution: List[List[str]]) -> None:
        self._raise_if_the_game_has_not_started_yet()

        if player not in self._players:
            raise ValueError(f"{player} is not currently playing")

        if player in self._rounds[self.current_round]:
            raise ValueError(f"{player} has already submitted a solution for the round")

        submission = Submission(player=player, solution=solution)
        self._score_submission(submission=submission)

    def _score_submission(self, submission: Submission) -> None:
        scores = {}
        try:
            self._validate_submission(submission=submission)
            for word in submission.get_words():
                score = sum(self._current_draw[letter]["points"] for letter in word)
                scores[word] = score
        finally:
            self._rounds[self.current_round][submission.player] = scores

    def _validate_submission(self, submission: Submission) -> None:
        validators = []

        letters = [
            letter
            for letter, info in self._current_draw.items()
            for _ in range(info["count"])
        ]
        validators.append(FromLettersValidator(letters=letters))

        used_words = [
            word
            for round_scores in self._rounds.values()
            for word in round_scores.get(submission.player, {}).keys()
        ]
        validators.append(NewWordValidator(used_words=used_words))

        for validator in validators:
            validator.validate(submission=submission)

    def get_word_scores(self, round: Optional[int] = None) -> Dict[str, Dict[str, Any]]:
        """Get word scores.

        Args:
            round: Round for which to get the scores. If None the scores for
                all rounds are returned.

        Raises:
            ValueError: If the requested round has not been played yet.

        Returns:
            Word scores for all players even if they haven't submitted.
                "words": {
                    "Cherry": {"HI": 2, "HELLO": 5},
                    "Davide": {},
                }
        """
        scores = {player: {} for player in self._players}
        if round is None:
            rounds_scores = self._rounds.values()
        else:
            try:
                rounds_scores = [self._rounds[round]]
            except KeyError as error:
                raise ValueError(f"Round {round} has not been played yet") from error
        for round_scores in rounds_scores:
            for player, word_scores in round_scores.items():
                for word, score in word_scores.items():
                    scores[player][word] = score
        return scores

    def get_total_scores(self, round: Optional[int] = None) -> Dict[str, int]:
        """Get total scores.

        Args:
            round: Round for which to get the scores. If None the scores for
                all rounds are returned.

        Returns:
            Total scores for all players even if they haven't submitted.
                {
                    "Cherry": 7,
                    "Davide": 0,
                }
        """
        scores = {player: 0 for player in self._players}
        if round is None:
            rounds_scores = self._rounds.values()
        else:
            try:
                rounds_scores = [self._rounds[round]]
            except KeyError as error:
                raise ValueError(f"Round {round} has not been played yet") from error
        for round_scores in rounds_scores:
            for player, word_scores in round_scores.items():
                scores[player] += sum(word_scores.values())
        return scores

    def _raise_if_the_game_has_not_started_yet(self) -> None:
        if not self._rounds:
            raise errors.WordylibError("Game has not started yet, draw first")
