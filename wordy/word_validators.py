from abc import ABC, abstractmethod
from collections import Counter
import re

from wordy.errors import InvalidWord


class WordValidator(ABC):
    @abstractmethod
    def validate(self, word):
        pass


class OneWordValidator(WordValidator):
    """Validate that a word is made up of one single word, without hyphens."""

    _ONE_WORD_PATTERN = r"^[A-zÀ-ÿ]+$"

    def validate(self, word):
        is_valid = bool(re.search(pattern=self._ONE_WORD_PATTERN, string=word))
        if not is_valid:
            raise InvalidWord(f'"{word}" is not a simple word')


class MinLengthValidator(WordValidator):
    """Validate that a word has minimum number of characters."""

    def __init__(self, min_length):
        """Instantiate validator.

        Args:
            min_length (int): Minimum expected word length.
        """
        self._min_length = min_length

    def validate(self, word):
        """Validate word.

        Args:
            word (str): Word.

        Raises:
            InvalidWord: If word is too short.
        """

        is_valid = len(word) >= self._min_length
        if not is_valid:
            raise InvalidWord(
                f'"{word}" is too short ' f"({len(word)} < {self._min_length})"
            )


class ExistingWordValidator(WordValidator):
    """Validate that a word exists."""

    def __init__(self, dictionary):
        """Instantiate validator.

        Args:
            dictionary (Dictionary): Language dictionary.
        """
        self._dictionary = dictionary

    def validate(self, word):
        """Validate word.

        Args:
            word (str): Word.

        Raises:
            InvalidWord: If word doesn't exist in dictionary.
        """

        is_valid = word in self._dictionary
        if not is_valid:
            raise InvalidWord(f'"{word}" does not exist')
