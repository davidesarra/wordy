import abc
from collections import Counter
from typing import List

from wordy.submission import Submission
from wordy.errors import InvalidSubmission
from wordy.utils import get_duplicates, has_duplicates, join


class SubmissionValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, submission: Submission) -> None:
        pass


class NoDuplicatesValidator(SubmissionValidator):
    """Validate that the solution has no duplicate words."""

    def validate(self, submission: Submission) -> None:
        words = submission.get_words()
        if has_duplicates(items=words):
            duplicate_words = get_duplicates(items=words)
            raise InvalidSubmission(
                f"Words {join(duplicate_words)} appear twice or more often"
            )


class OnlyNewWordsValidator(SubmissionValidator):
    """Validate that solution doesn't include words previously submitted by
    the same player.
    """

    def __init__(self, used_words):
        self._used_words = set(used_words)

    def validate(self, submission: Submission) -> None:
        submission_words = set(submission.get_words())
        reused_words = submission_words & self._used_words
        if reused_words:
            raise InvalidSubmission(
                f"Words {reused_words} have been previously used"
            )


class SubmissionFromLettersValidator(SubmissionValidator):
    """Validate that the submitted words could be formed from the letter draw."""

    def __init__(self, letters: List[str]) -> None:
        """Instantiate validator.

        Args:
            letters: Drawn letters.
        """
        self._stock_letters = [letter.upper() for letter in letters]

    def validate(self, submission: Submission) -> None:
        """Validate that the submission can be created from the drawn letters.

        Args:
            submission: Submission.

        Raises:
            InvalidSubmission: If the words couldn't have been formed from
                the letter draw.
        """
        if not submission:
            return
        balance: Counter = Counter(self._stock_letters)
        used_letters = [letter.upper() for letter in submission.get_letters()]
        usage = Counter(used_letters)
        balance.subtract(usage)
        overused_letters = {
            letter for letter, letter_balance in balance.items() if letter_balance < 0
        }
        if overused_letters:
            raise InvalidSubmission(
                f"Letter(s) {join(overused_letters)} have been overused"
            )
