import pytest

from wordylib import errors
from wordylib.submission import Submission
from wordylib.validators import FromLettersValidator, NewWordValidator


class TestFromLettersValidator:
    def test_validate_valid_submission(self):
        # given
        letters = ["H", "I", "I", "T", "K"]
        submission = Submission(
            player="Davide", solution=[["H", "I", "T"], ["I", " ", " "]]
        )

        # when and then
        validator = FromLettersValidator(letters=letters)
        validator.validate(submission=submission)

    def test_validate_invalid_submission(self):
        # given
        letters = ["H", "I", "I", "T", "K"]
        submission = Submission(
            player="Davide", solution=[["H", "A", "T"], ["I", " ", " "]]
        )

        # when and then
        validator = FromLettersValidator(letters=letters)
        expected_msg = r"^Some letters were used too many times \(A\)$"
        with pytest.raises(errors.InvalidSubmission, match=expected_msg):
            validator.validate(submission=submission)


class TestNewWordValidator:
    def test_validate_valid_submission(self):
        # given
        used_words = {"HITS"}
        submission = Submission(
            player="Davide", solution=[["H", "I", "T"], ["I", " ", " "]]
        )

        # when and then
        validator = NewWordValidator(used_words=used_words)
        validator.validate(submission=submission)

    def test_validate_invalid_submission(self):
        # given
        used_words = {"HIT"}
        submission = Submission(
            player="Davide", solution=[["H", "I", "T"], ["I", " ", " "]]
        )

        # when and then
        validator = NewWordValidator(used_words=used_words)
        expected_msg = r"^Some words were already used \(HIT\)$"
        with pytest.raises(errors.InvalidSubmission, match=expected_msg):
            validator.validate(submission=submission)
