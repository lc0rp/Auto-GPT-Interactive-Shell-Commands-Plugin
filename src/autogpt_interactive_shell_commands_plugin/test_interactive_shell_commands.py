from unittest.mock import patch
from .interactive_shell_commands import InteractiveShellCommands


def test_ask_user() -> None:
    prompts = ["Question 1: ", "Question 2: ", "Question 3: "]
    expected_responses = ["Answer 1", "Answer 2", "Answer 3"]
    with patch("inputimeout.inputimeout", side_effect=expected_responses):
        is_commands = InteractiveShellCommands(default_timeout_seconds=10)
        responses = is_commands.ask_user(prompts)

    assert (
        responses == expected_responses
    ), f"Expected {expected_responses} but got {responses}"


def test_ask_user_timeout() -> None:
    prompts = ["Prompt 1:"]
    timeout = 5

    from inputimeout import TimeoutOccurred

    with patch("inputimeout.inputimeout", side_effect=TimeoutOccurred):
        is_commands = InteractiveShellCommands(default_timeout_seconds=10)
        responses = is_commands.ask_user(prompts, timeout)

    assert responses == [f"Timeout after {timeout} seconds"]
