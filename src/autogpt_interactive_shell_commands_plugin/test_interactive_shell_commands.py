import pytest
from io import StringIO
from unittest.mock import patch
from .interactive_shell_commands import ask_user


def test_ask_user():
    prompts = ["Question 1: ", "Question 2: ", "Question 3: "]
    expected_responses = ["Answer 1", "Answer 2", "Answer 3"]

    with patch("builtins.input", side_effect=expected_responses):
        responses = ask_user(prompts)

    assert (
        responses == expected_responses
    ), f"Expected {expected_responses} but got {responses}"
