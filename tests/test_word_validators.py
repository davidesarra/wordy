import pytest

from wordy.errors import InvalidWord
from wordy.word_validators import (
    ExistingWordValidator,
    WordFromLettersValidator,
    OneWordValidator,
    MinLengthValidator,
)


@pytest.mark.parametrize("word", ["a", "apple", "perché", "françois"])
def test_one_word_validator_true(word):
    validator = OneWordValidator()
    validator.validate(word=word)


@pytest.mark.parametrize("word", ["", "a apple", "a green apple", "sugar-free"])
def test_one_word_validator_raises(word):
    validator = OneWordValidator()
    with pytest.raises(InvalidWord):
        validator.validate(word=word)


@pytest.mark.parametrize("word,min_length", [("", 0), ("a", 0), ("a", 1), ("four", 4),])
def test_min_length_validator_true(word, min_length):
    validator = MinLengthValidator(min_length=min_length)
    validator.validate(word=word)


@pytest.mark.parametrize("word,min_length", [("", 1), ("a", 2), ("four", 5),])
def test_min_length_validator_raises(word, min_length):
    validator = MinLengthValidator(min_length=min_length)
    with pytest.raises(InvalidWord):
        validator.validate(word=word)


@pytest.mark.parametrize("word,letters", [("home", "hhimseo"),])
def test_from_letters_validator_true(word, letters):
    validator = WordFromLettersValidator(letters=letters)
    validator.validate(word=word)


@pytest.mark.parametrize("word,letters", [("home", "hhimse"), ("chess", "jecsh"),])
def test_from_letters_validator_raises(word, letters):
    validator = WordFromLettersValidator(letters=letters)
    with pytest.raises(InvalidWord):
        validator.validate(word=word)


@pytest.mark.parametrize(
    "word,dictionary",
    [  # dictionary argument mocked with list due to expected similar behaviour
        ("home", ["hat", "home"]),
    ],
)
def test_existing_word_validator_true(word, dictionary):
    validator = ExistingWordValidator(dictionary=dictionary)
    validator.validate(word=word)


@pytest.mark.parametrize(
    "word,dictionary",
    [  # dictionary argument mocked with list due to expected similar behaviour
        ("home", ["hat", "cat"]),
    ],
)
def test_existing_word_validator_raises(word, dictionary):
    validator = ExistingWordValidator(dictionary=dictionary)
    with pytest.raises(InvalidWord):
        validator.validate(word=word)
