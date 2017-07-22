import pytest

from wordy.errors import InvalidSubmission, InvalidWord
from wordy.meta_validators import MetaSubmissionValidator, MetaWordValidator
from wordy.scoreboard import Submission
from wordy.submission_validators import NoDuplicatesValidator, OnlyNewWordsValidator
from wordy.word_validators import MinLengthValidator, OneWordValidator


@pytest.mark.parametrize(
    "validators,word",
    [
        ([MinLengthValidator(min_length=1), OneWordValidator(),], "a"),
        ([MinLengthValidator(min_length=1), OneWordValidator(),], "an"),
        ([MinLengthValidator(min_length=2), OneWordValidator(),], "an"),
    ],
)
def test_meta_word_validator_true(validators, word):
    meta_validator = MetaWordValidator(validators=validators)
    meta_validator.validate(word=word)


@pytest.mark.parametrize(
    "validators,word",
    [
        ([MinLengthValidator(min_length=1), OneWordValidator(),], "a hat"),
        ([MinLengthValidator(min_length=10), OneWordValidator(),], "hat"),
    ],
)
def test_meta_word_validator_raises(validators, word):
    meta_validator = MetaWordValidator(validators=validators)
    with pytest.raises(InvalidWord):
        meta_validator.validate(word=word)


@pytest.mark.parametrize(
    "validators,solution",
    [
        (
            [OnlyNewWordsValidator(used_words=["he", "hat"]), NoDuplicatesValidator(),],
            Submission(player="Jim", words=[]),
        ),
        (
            [OnlyNewWordsValidator(used_words=["he", "hat"]), NoDuplicatesValidator(),],
            Submission(player="Jim", words=["hi", "hello"]),
        ),
    ],
)
def test_meta_submission_validator_true(validators, submission):
    meta_validator = MetaSubmissionValidator(validators=validators)
    meta_validator.validate(submission=submission)


@pytest.mark.parametrize(
    "validators,solution",
    [
        (
            [OnlyNewWordsValidator(used_words=["he", "hat"]), NoDuplicatesValidator(),],
            Submission(player="Jim", words=["hat"]),
        ),
        (
            [OnlyNewWordsValidator(used_words=["he", "hat"]), NoDuplicatesValidator(),],
            Submission(player="Jim", words=["had", "had"]),
        ),
    ],
)
def test_meta_submission_validator_raise(validators, submission):
    meta_validator = MetaSubmissionValidator(validators=validators)
    with pytest.raises(InvalidSubmission):
        meta_validator.validate(submission=submission)
