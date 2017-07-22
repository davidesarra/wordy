import pytest

from wordy.interface import Interface


@pytest.mark.parametrize(
    "message,inputs,expected",
    [
        ("Enter your input: ", ["abc123!"], "abc123!"),
        ("Enter your input: ", ["123"], "123"),
        ("Enter your input: ", ['!"£$'], '!"£$'),
        ("Enter your input: ", [""], ""),
        ("Enter your input: ", ["", "abc123!"], ""),
        ("", ["first", "second"], "first"),
    ],
)
def test_interface_get_non_empty_input(mocker, message, inputs, expected):
    input_mocker = mocker.patch("builtins.input", side_effect=inputs)
    result = Interface()._get_any_input(message=message)
    assert result == expected
    input_mocker.assert_called_with(message)


@pytest.mark.parametrize(
    "message,inputs,expected",
    [
        ("Enter your input: ", ["abc123!"], "abc123!"),
        ("Enter your input: ", ["123"], "123"),
        ("Enter your input: ", ['!"£$'], '!"£$'),
        ("Enter your input: ", ["", "", "abc123!"], "abc123!"),
        ("Enter your input: ", ["first", "second"], "first"),
        ("", ["", "first", "second"], "first"),
    ],
)
def test_interface_get_non_empty_input(mocker, message, inputs, expected):
    input_mocker = mocker.patch("builtins.input", side_effect=inputs)
    result = Interface()._get_non_empty_input(message=message)
    assert result == expected
    input_mocker.assert_called_with(message)


@pytest.mark.parametrize(
    "message,mandatory,inputs,expected",
    [
        ("Type: ", True, ["abc123!"], "abc123!"),
        ("Type: ", True, ["123"], "123"),
        ("Type: ", True, ['!"£$'], '!"£$'),
        ("Type: ", True, ["", "", "abc123!"], "abc123!"),
        ("Type: ", False, ["", "", "abc123!"], ""),
        ("Type: ", True, ["first", "second"], "first"),
    ],
)
def test_interface_get_string(mocker, message, mandatory, inputs, expected):
    input_mocker = mocker.patch("builtins.input", side_effect=inputs)
    result = Interface().get_string(message=message, mandatory=mandatory)
    assert result == expected
    input_mocker.assert_called_with(message)


@pytest.mark.parametrize(
    "message,mandatory,inputs,expected",
    [
        ("Type: ", True, ["123"], 123),
        ("Type: ", True, ["0.1", ".1", "1"], 1),
        ("Type: ", True, ["0123"], 123),
        ("Type: ", True, ["abc123!", "", "1", "2"], 1),
        ("Type: ", True, ["1", "2"], 1),
        ("Type: ", False, ["abc123!", "", "1", "2"], None),
    ],
)
def test_interface_get_integer(mocker, message, mandatory, inputs, expected):
    input_mocker = mocker.patch("builtins.input", side_effect=inputs)
    result = Interface().get_integer(message=message, mandatory=mandatory)
    assert result == expected
    input_mocker.assert_called_with(message)


@pytest.mark.parametrize(
    "message,true_values,false_values,inputs,expected",
    [
        ("Type: ", {"yes", "y"}, {"n"}, ["1", "", "y"], True),
        ("Type: ", {"yes", "y"}, {"n"}, ["1", "ye s", "n"], False),
    ],
)
def test_interface_get_boolean(
    mocker, message, true_values, false_values, inputs, expected
):
    input_mocker = mocker.patch("builtins.input", side_effect=inputs)
    result = Interface().get_boolean(
        message=message, true_values=true_values, false_values=false_values
    )
    assert result == expected
    input_mocker.assert_called_with(message)
    assert input_mocker.call_count == len(inputs)


@pytest.mark.parametrize(
    "message,separator,strip_whitespace,mandatory,input_value,expected",
    [
        (
            "Type: ",
            ",",
            True,
            True,
            "apple juice,   Tim  T. Jon , 123! ",
            ["apple juice", "Tim  T. Jon", "123!"],
        ),
        ("Type: ", ",", True, True, "just a block", ["just a block"]),
        ("Type: ", ",", True, True, " , Light", ["", "Light"]),
        ("Type: ", ",", False, True, " , Light", [" ", " Light"]),
        ("Type: ", ",", False, False, "something", ["something"]),
        ("Type: ", ",", False, False, "", []),
    ],
)
def test_interface_get_list_of_strings(
    mocker, message, separator, strip_whitespace, mandatory, input_value, expected
):
    input_mocker = mocker.patch("builtins.input", return_value=input_value)
    result = Interface().get_list_of_strings(
        message=message,
        separator=separator,
        strip_whitespace=strip_whitespace,
        mandatory=mandatory,
    )
    assert result == expected
    input_mocker.assert_called_once_with(message)
