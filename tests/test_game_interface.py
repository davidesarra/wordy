import pytest

from wordy.errors import InvalidTitle
from wordy.game_interface import GameInterface, Header


@pytest.mark.parametrize(
    "title,expected",
    [
        ("a", "=========== a ==========="),
        ("EVEN TITLE", "============== EVEN TITLE =============="),
        ("ODD TITLE", "============ ODD TITLE ============ "),
        (
            "LONG TITLEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",
            "====== LONG TITLEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE ====== ",
        ),
    ],
)
def test_header(title, expected):
    assert Header(title=title) == expected


@pytest.mark.parametrize("title", ["", "TOO LONG TITLE" + "E" * 66,])
def test_header_with_invalid_title(title):
    with pytest.raises(InvalidTitle):
        Header(title=title)


def test_game_interface_get_submissions(mocker):
    mocker.patch("builtins.input", side_effect=["", "hell", "hi, hello"])
    interface = GameInterface()
    result = interface.get_solutions(player_names=["Jim", "Greg", "Tom"])
    expected = dict(Jim=[], Greg=["hell"], Tom=["hi", "hello"])
    assert result == expected
