import random

import pytest

from wordylib.alphabet import Alphabet


@pytest.fixture
def letter_frequency():
    return {
        "a": 0.0816708167081671,
        "b": 0.014920149201492018,
        "c": 0.027820278202782038,
        "d": 0.04253042530425305,
        "e": 0.12702127021270215,
        "f": 0.02228022280222803,
        "g": 0.020150201502015026,
        "h": 0.06094060940609408,
        "i": 0.06966069660696608,
        "j": 0.0015300153001530019,
        "k": 0.007720077200772011,
        "l": 0.040250402504025055,
        "m": 0.02406024060240603,
        "n": 0.06749067490674908,
        "o": 0.0750707507075071,
        "p": 0.019290192901929026,
        "q": 0.0009500095000950012,
        "r": 0.05987059870598708,
        "s": 0.06327063270632707,
        "t": 0.09056090560905611,
        "u": 0.027580275802758035,
        "v": 0.009780097800978013,
        "w": 0.02360023600236003,
        "x": 0.001500015000150002,
        "y": 0.019740197401974025,
        "z": 0.0007400074000740009,
    }


def test_alphabet_from_data(letter_frequency):
    # given
    expected = letter_frequency

    # when
    result = Alphabet.from_data(language_code="en")

    # then
    assert result.letter_frequency == expected


def test_alphabet_draw(letter_frequency):
    # given
    random.seed(10)
    num_letters = 3
    expected = {"n": {"count": 2, "points": 1}, "i": {"count": 1, "points": 1}}

    # when
    alphabet = Alphabet(letter_frequency=letter_frequency)
    result = alphabet.draw(num_letters=num_letters)

    # then
    assert result == expected
