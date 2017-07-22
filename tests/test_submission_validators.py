import pytest

from wordy.errors import InvalidSubmission
from wordy.scoreboard import Submission
from wordy.submission_validators import (
    NoDuplicatesValidator,
    SubmissionFromLettersValidator,
)


@pytest.mark.parametrize(
    "solution",
    [
        Submission(player="Jim", words=[]),
        Submission(player="Jim", words=[""]),
        Submission(player="Jim", words=["apple"]),
        Submission(player="Jim", words=["apple", "app"]),
        Submission(player="Jim", words=["perche", "perché"]),
    ],
)
def test_no_duplicates_validator_true(submission):
    validator = NoDuplicatesValidator()
    validator.validate(submission=submission)


@pytest.mark.parametrize(
    "solution",
    [
        Submission(player="Jim", words=["", "", "apple"]),
        Submission(player="Jim", words=["apple", "app", "apple"]),
    ],
)
def test_no_duplicates_validator_raises(submission):
    validator = NoDuplicatesValidator()
    with pytest.raises(InvalidSubmission):
        validator.validate(submission=submission)


@pytest.mark.parametrize(
    "solution,letters",
    [
        (Submission(player="Jim", words=[]), "hellogl"),
        (Submission(player="Jim", words=["h"]), "hellogl"),
        (Submission(player="Jim", words=["hello"]), "hellogl"),
        (Submission(player="Jim", words=["hello", "gel"]), "hellogl"),
        (
            Submission(player="Jim", words=["pant", "per", "rib", "id", "she"]),
            "tsenrifbphad",
        ),
        (Submission(player="Jim", words=["hello", "hello"]), "hellogl"),
    ],
)
def test_submission_from_letters_validator_true(submission, letters):
    validator = SubmissionFromLettersValidator(letters=letters)
    validator.validate(submission=submission)


@pytest.mark.parametrize(
    "solution,letters",
    [(Submission(player="Jim", words=["hello", "gel", "leg", "log"]), "hellogl"),],
)
def test_submission_from_letters_validator_raises(submission, letters):
    validator = SubmissionFromLettersValidator(letters=letters)
    with pytest.raises(InvalidSubmission):
        validator.validate(submission=submission)
