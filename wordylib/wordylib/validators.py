import abc
import collections
from typing import List


from wordylib import errors
from wordylib.submission import Submission


class BaseValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, submission: Submission) -> None:
        pass


class FromLettersValidator(BaseValidator):
    def __init__(self, letters: List[str]) -> None:
        self.letters = letters

    def validate(self, submission: Submission) -> None:
        used_letters = submission.get_letters()
        usage = collections.Counter(used_letters)
        balance = collections.Counter(self.letters)
        balance.subtract(usage)
        overused_letters = {
            letter for letter, letter_balance in balance.items() if letter_balance < 0
        }
        if overused_letters:
            raise errors.InvalidSubmission(
                f"Some letters were used too many times ({', '.join(overused_letters)})"
            )


class NewWordValidator(BaseValidator):
    def __init__(self, used_words: List[str]) -> None:
        self.used_words = set(used_words)

    def validate(self, submission: Submission) -> None:
        submission_words = set(submission.get_words())
        reused_words = self.used_words & submission_words
        if reused_words:
            raise errors.InvalidSubmission(
                f"Some words were already used ({', '.join(reused_words)})"
            )
