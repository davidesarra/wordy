from collections import namedtuple
from typing import Dict, List, Union

from wordy.errors import InvalidPlayerName
from wordy.submission import Submission
from wordy.letters import Alphabet
from wordy.submission_validators import (
    NoDuplicatesValidator,
    OnlyNewWordsValidator,
    SubmissionFromLettersValidator,
)
from wordy.utils import has_duplicates
from wordy.word_dictionaries import Dictionary
from wordy.word_validators import (
    ExistingWordValidator,
    OneWordValidator,
    MinLengthValidator,
)


Score = namedtuple("Score", ["player", "round", "word", "points"])


class Scorer:
    def __init__(self, letter_draw):
        """Instantiate Scorer.

        Args:
            letter_draw (list<Letter>): Drawn letters.
        """
        self.points_by_letter = {letter.letter: letter.points for letter in letter_draw}

    def score_word(self, word: str):
        """Score word.

        Args:
            word (str): Word.

        Returns:
            int: Points.
        """
        return sum(self.points_by_letter.get(letter, 0) for letter in word)


class Scoreboard(object):
    def __init__(self, players: List[str], language: str) -> None:
        """Initialize scoreboard.

        Args:
            players: Player names.
            language: Language.

        Raises:
            InvalidPlayerName: If player names aren't unique.
        """
        if has_duplicates(items=players):
            raise InvalidPlayerName("Player names must be unique")
        self.players = players
        self._alphabet = Alphabet(language=language)
        self._dictionary = Dictionary(language=language)
        self.current_round = 0
        self.current_letter_draw = None
        self._scores: List[Score] = []

    def start_round(self) -> None:
        """Start a new round."""
        self.current_round += 1
        self.current_letter_draw = self._alphabet.draw_letters()

    def score(self, player: str, solution: List[List[str]]):
        """Score round word submissions.

        Args:
            player: Player.
            solution: Submitted 2D solution canvas.

        Returns:
            str: If the submission or any submitted word is invalid.

        Raises:
            InvalidPlayerName: If `player` is not among the players.
        """
        if player not in self.players:
            raise InvalidPlayerName(f"{player} isn't playing")

        submission = Submission(player=player, solution=solution)
        if not solution:
            return

        self._validate_submission(submission=submission)
        scorer = Scorer(letter_draw=self.current_letter_draw)
        scores = []
        for word in submission.get_words():
            self._validate_word(word=word)
            points = scorer.score_word(word=word)
            score = Score(
                player=player, round=self.current_round, word=word, points=points,
            )
            scores.append(score)
        self._scores.extend(scores)

    def _validate_submission(self, submission: Submission) -> None:
        validators = [
            SubmissionFromLettersValidator(
                letters=[letter.letter for letter in self.current_letter_draw]
            ),
            NoDuplicatesValidator(),
            OnlyNewWordsValidator(
                used_words=[
                    score.word
                    for score in self._scores
                    if score.player == submission.player
                ]
            ),
        ]
        for validator in validators:
            validator.validate(submission=submission)

    def _validate_word(self, word: str) -> None:
        validators = [
            OneWordValidator(),
            MinLengthValidator(min_length=self._alphabet.MIN_WORD_LENGTH),
            ExistingWordValidator(dictionary=self._dictionary),
        ]
        for validator in validators:
            validator.validate(word=word)

    def get_current_round_word_scores(self) -> List[Dict[str, Union[str, int]]]:
        """Get word by word scores for current round.

        Returns:
            Word scores.
        """
        return [
            dict(player=score.player, word=score.word, points=score.points)
            for score in self._scores
            if score.round == self.current_round
        ]

    def get_current_round_total_scores(self):
        """Get total scores by player for current round.

        Returns:
            Total scores by player for current round.
        """
        total_scores = {}
        for player in self.players:
            total_scores[player] = 0
        for score in self._scores:
            if score.round == self.current_round:
                total_scores[score.player] += score.points
        return total_scores

    def get_total_scores(self) -> Dict[str, int]:
        """Get running total scores by player.

        Returns:
            Running total scores by player.
        """
        total_scores = {}
        for player in self.players:
            total_scores[player] = 0
        for score in self._scores:
            total_scores[score.player] += score.points
        return total_scores
