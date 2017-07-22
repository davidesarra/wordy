import pytest

from wordy.errors import UnsupportedLanguage
from wordy.word_dictionaries import Dictionary


def test_dictionary_with_invalid_language():
    with pytest.raises(UnsupportedLanguage):
        Dictionary(language="CK")


@pytest.mark.parametrize(
    "language,word,expected",
    [
        ("en", "apple", True),
        ("it", "apple", False),  # words' validity depends on the language
        ("en", "tyipo", False),  # typos are not valid words
        ("en", "fourty", False),  # common typos are not valid words
        ("it", "mela", True),  # support for multiple languages
        ("en", "mela", False),
        ("it", "errrore", False),
    ],
)
def test_dictionary_word_look_up(language, word, expected):
    dictionary = Dictionary(language=language)
    result = word in dictionary
    assert result is expected
