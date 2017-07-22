import pytest


from wordy.utils import get_duplicates, has_duplicates


@pytest.mark.parametrize(
    "sequence,expected",
    [
        ([], False),
        ([1, 2, 3], False),
        ([1, 2, 3, 3], True),
        (["a", "b", "c"], False),
        (["a", "b", "c", "c"], True),
    ],
)
def test_has_duplicates(sequence, expected):
    result = has_duplicates(sequence=sequence)
    assert result is expected


@pytest.mark.parametrize(
    "sequence,expected",
    [
        ([], []),
        ([1, 2, 3], []),
        ([1, 2, 3, 3], [3]),
        (["a", "b", "c"], []),
        (["a", "b", "c", "c"], ["c"]),
    ],
)
def test_get_duplicates(sequence, expected):
    result = list(get_duplicates(sequence=sequence))
    assert result == expected
