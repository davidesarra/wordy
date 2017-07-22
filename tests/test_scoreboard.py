from unittest.case import TestCase

import pytest

from wordy.errors import InvalidPlayerName
from wordy.scoreboard import Scoreboard, Scorer
from wordy.letters import Alphabet, Letter


@pytest.mark.parametrize(
    "word,expected", [("hotel", 7), ("hello", 8), ("zip", 0), ("", 0)]
)
def test_scorer(word, expected):
    letter_draw = [
        Letter(letter="h", points=2),
        Letter(letter="e", points=1),
        Letter(letter="l", points=2),
        Letter(letter="o", points=1),
        Letter(letter="t", points=1),
    ]
    scorer = Scorer(letter_draw=letter_draw)
    result = scorer.score_word(word=word)
    assert result == expected


def test_scoreboard_instantiated_correctly():
    players = ["Joe", "Mary May", "Tony T. Holmes"]
    scoreboard = Scoreboard(players=players, language="en")
    result = scoreboard.players
    expected = ["Joe", "Mary May", "Tony T. Holmes"]
    assert result == expected


def test_scoreboard_instantiated_with_duplicate_names():
    players = ["Mary May", "Mary May", "Tom"]
    with pytest.raises(InvalidPlayerName):
        Scoreboard(players=players, language="en")


def test_scoreboard_scores(mocker):
    mocker.patch.object(
        Alphabet,
        "draw_letters",
        side_effect=[
            [
                Letter(letter="c", points=2),
                Letter(letter="a", points=1),
                Letter(letter="r", points=1),
                Letter(letter="a", points=1),
                Letter(letter="t", points=5),
            ],
            [
                Letter(letter="h", points=1),
                Letter(letter="a", points=1),
                Letter(letter="t", points=5),
            ],
        ],
    )

    scoreboard = Scoreboard(players=["Jim", "Tom"], language="en")

    scoreboard.start_round()
    error = scoreboard.score(player="Jim", solution=["rat"])
    assert error is None
    error = scoreboard.score(player="Tom", solution=["car", "cat"])
    assert error is None
    result = scoreboard.get_current_round_word_scores()
    expected = [
        dict(player="Jim", points=7, word="rat"),
        dict(player="Tom", points=4, word="car"),
        dict(player="Tom", points=8, word="cat"),
    ]
    TestCase().assertCountEqual(first=result, second=expected)
    result = scoreboard.get_current_round_total_scores()
    expected = {"Jim": 7, "Tom": 12}
    assert result == expected

    scoreboard.start_round()
    error = scoreboard.score(player="Jim", solution=["hat", "hat"])
    assert error is not None
    error = scoreboard.score(player="Tom", solution=[])
    assert error is None
    result = scoreboard.get_current_round_word_scores()
    expected = []
    TestCase().assertCountEqual(first=result, second=expected)

    result = scoreboard.get_current_round_total_scores()
    expected = {"Jim": 0, "Tom": 0}
    assert result == expected

    result = scoreboard.get_total_scores()
    expected = {"Jim": 7, "Tom": 12}
    assert result == expected
