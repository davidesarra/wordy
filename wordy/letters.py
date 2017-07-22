import json
import random
from collections import namedtuple
from typing import Any, Dict, List

from wordy.errors import UnsupportedLanguage


Letter = namedtuple("Letter", ["letter", "points"])


class Alphabet:
    _MIN_POINTS = 1
    _MAX_POINTS = 12
    _DRAW_SIZE = 12
    MIN_WORD_LENGTH = 2

    def __init__(self, language: str) -> None:
        self.language = language
        self._letters = self._get_letters(language=language)
        self._draw_probabilities = self._get_draw_probabilities(language=language)
        self._points_by_letter = self._get_points_by_letter()

    def _get_points_by_letter(self):
        def get_points(
            draw_probability,
            draw_size=self._DRAW_SIZE,
            min_points=self._MIN_POINTS,
            max_points=self._MAX_POINTS,
        ):
            raw_points = 1 / draw_probability / draw_size
            return int(min(max(raw_points, min_points), max_points))

        return {
            letter: get_points(draw_probability=draw_probability)
            for letter, draw_probability in zip(self._letters, self._draw_probabilities)
        }

    def draw_letters(self):
        """Draw letters.

        Returns:
            list<Letter>: Drawn letters.
        """
        letter_draw = random.choices(
            population=self._letters,
            weights=self._draw_probabilities,
            k=self._DRAW_SIZE,
        )
        return [
            Letter(letter=letter.upper(), points=self._points_by_letter[letter])
            for letter in letter_draw
        ]

    def _get_letters(self, language: str) -> List[str]:
        language_cache = self._get_language_data(language=language)
        return [letter.upper() for letter in language_cache.keys()]

    def _get_draw_probabilities(self, language: str) -> List[int]:
        language_cache = self._get_language_data(language=language)
        return [language_cache[letter.lower()] for letter in self._letters]

    @staticmethod
    def _get_language_data(language) -> Dict[str, Any]:
        with open(file="data/languages.json", mode="r") as file:
            languages_cache = json.load(file)

        try:
            return languages_cache[language]
        except KeyError:
            supported_languages = [*languages_cache.keys()]
            raise UnsupportedLanguage(
                f"{language} is unsupported, choose among {supported_languages}"
            )
