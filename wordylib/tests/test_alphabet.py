import random

import pytest

from wordylib.alphabet import Alphabet


@pytest.fixture
def letter_frequency():
    return {
        "A": 0.0816708167081671,
        "B": 0.014920149201492018,
        "C": 0.027820278202782038,
        "D": 0.04253042530425305,
        "E": 0.12702127021270215,
        "F": 0.02228022280222803,
        "G": 0.020150201502015026,
        "H": 0.06094060940609408,
        "I": 0.06966069660696608,
        "J": 0.0015300153001530019,
        "K": 0.007720077200772011,
        "L": 0.040250402504025055,
        "M": 0.02406024060240603,
        "N": 0.06749067490674908,
        "O": 0.0750707507075071,
        "P": 0.019290192901929026,
        "Q": 0.0009500095000950012,
        "R": 0.05987059870598708,
        "S": 0.06327063270632707,
        "T": 0.09056090560905611,
        "U": 0.027580275802758035,
        "V": 0.009780097800978013,
        "W": 0.02360023600236003,
        "X": 0.001500015000150002,
        "Y": 0.019740197401974025,
        "Z": 0.0007400074000740009,
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

    # when
    alphabet = Alphabet(letter_frequency=letter_frequency)
    result = alphabet.draw(num_letters=num_letters)

    # then
    expected = {"N": {"count": 2, "points": 1}, "I": {"count": 1, "points": 1}}
    assert result == expected
