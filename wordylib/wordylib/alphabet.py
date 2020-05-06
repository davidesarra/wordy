import collections
import json
import pathlib
import math
import random
from typing import Dict


class Alphabet:
    def __init__(self, letter_frequency: Dict[str, float]) -> None:
        self.letter_frequency = letter_frequency

    @classmethod
    def from_data(cls, language_code: str) -> "Alphabet":
        data_path = pathlib.Path(__file__).parent / "data/letter_frequency.json"
        language_data = json.loads(data_path.read_text())[language_code]
        return cls(letter_frequency=language_data)

    def draw(self, num_letters: int) -> Dict[str, Dict[str, int]]:
        letters = []
        frequencies = []
        for letter, frequency in self.letter_frequency.items():
            letters.append(letter)
            frequencies.append(frequency)

        drawn_letters = random.choices(
            population=letters, weights=frequencies, k=num_letters,
        )
        draw_letters_counter = collections.Counter(drawn_letters)
        return {
            letter: {"count": count, "points": self._get_points(letter=letter)}
            for letter, count in draw_letters_counter.items()
        }

    def _get_points(self, letter: str) -> int:
        min_points = 1
        max_points = 9
        k = 0.015  # this steepness works well with the English language
        x = self.letter_frequency[letter]
        logistic_function = 1 / (1 + math.exp(-k * x))
        rescaled_logistic_function = (logistic_function - 0.5) * 2
        return round(max(rescaled_logistic_function * max_points, min_points))
