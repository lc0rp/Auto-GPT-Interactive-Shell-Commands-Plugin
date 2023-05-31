"""
Tests for the InteractiveShellCommands class.
"""
from unittest.mock import patch

from . import AutoGPTInteractiveShellCommandsPlugin
from .interactive_shell_commands import InteractiveShellCommands
from auto_gpt_plugin_template import AutoGPTPluginTemplate

def test_ask_user() -> None:
    """ Test that the ask_user method returns the expected responses."""
    prompts = ["Question 1: ", "Question 2: ", "Question 3: "]
    expected_responses = ["Answer 1", "Answer 2", "Answer 3"]
    with patch("inputimeout.inputimeout", side_effect=expected_responses):
        is_commands = InteractiveShellCommands(default_timeout_seconds=10)
        responses = is_commands.ask_user(prompts)

    assert (
        responses == expected_responses
    ), f"Expected {expected_responses} but got {responses}"


def test_ask_user_timeout() -> None:
    """ Test that the ask_user method returns the expected responses when a timeout occurs."""
    prompts = ["Prompt 1:"]
    timeout = 5

    from inputimeout import TimeoutOccurred

    with patch("inputimeout.inputimeout", side_effect=TimeoutOccurred):
        is_commands = InteractiveShellCommands(default_timeout_seconds=10)
        responses = is_commands.ask_user(prompts, timeout)

    assert responses == [f"Timeout after {timeout} seconds"]


def test_auto_gpt_interactive_shell_commands_plugin():
    plugin = AutoGPTInteractiveShellCommandsPlugin()

    assert isinstance(plugin, AutoGPTPluginTemplate)
    assert plugin._name == "Auto-GPT-Interactive-Shell-Commands-Plugin"

    assert plugin.can_handle_post_prompt() is True
    assert plugin.can_handle_on_response() is False
    assert plugin.can_handle_on_planning() is False
    assert plugin.can_handle_post_planning() is False
    assert plugin.can_handle_pre_instruction() is False
    assert plugin.can_handle_on_instruction() is False
    assert plugin.can_handle_post_instruction() is False
    assert plugin.can_handle_pre_command() is False
    assert plugin.can_handle_post_command() is False
    messages = []
    model = None
    temperature = 1.0
    max_tokens = 10
    assert plugin.can_handle_chat_completion(messages, model, temperature, max_tokens) is False
    text = ""
    assert plugin.can_handle_text_embedding(text) is False
    user_input = ""
    assert plugin.can_handle_user_input(user_input) is False
    assert plugin.can_handle_report() is False