import pytest

from wordy.letters import Alphabet
from wordy.errors import UnsupportedLanguage


def test_alphabet_with_invalid_language():
    with pytest.raises(UnsupportedLanguage):
        Alphabet(language="ck")


def test_alphabet_letter_draw_has_required_length():
    alphabet = Alphabet(language="en")
    assert len(alphabet.draw_letters()) == 12


def test_alphabet_letter_draw_is_random():
    alphabet = Alphabet(language="en")
    first_draw = alphabet.draw_letters()
    second_draw = alphabet.draw_letters()
    # given that the outcome is probabilist, the assertion may fail sometimes
    assert first_draw != second_draw
