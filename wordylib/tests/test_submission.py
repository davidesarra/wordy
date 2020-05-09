from wordylib.submission import Submission


def test_submission_get_letters():
    # given
    player = "Davide"
    solution = [["h", "I"], ["A", " "], ["T", " "]]

    # when
    submission = Submission(player=player, solution=solution)
    result = submission.get_letters()

    # then
    expected = ["H", "I", "A", "T"]
    assert sorted(result) == sorted(expected)


def test_submission_get_words():
    # given
    player = "Davide"
    solution = [["h", "I"], ["A", " "], ["T", " "]]

    # when
    submission = Submission(player=player, solution=solution)
    result = submission.get_words()

    # then
    expected = ["HI", "HAT"]
    assert sorted(result) == sorted(expected)
