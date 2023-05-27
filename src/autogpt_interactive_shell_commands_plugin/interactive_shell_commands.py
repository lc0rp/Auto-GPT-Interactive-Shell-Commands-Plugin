"""Execute interactive shell commands in the workspace"""
import os
import socket
import subprocess
import sys
import select

# from autogpt.config import Config

# CFG = Config()


def read_input():
    return os.read(sys.stdin.fileno(), 1024)


def execute_interactive_shell(command_line: str) -> list[dict]:
    """Execute a shell command that requires interactivity and return the output

    Args:
        command_line (str): The command line to execute

    Returns:
        list[dict]: The interaction between the user and the process, as a list of dictionaries: [{role: "user"|"process"|"error", content: "the content of the interaction"}, ...]
    """
    process = subprocess.Popen(
        command_line,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # To capture the conversation, we'll read from one set of descriptors, save the output and write it to the other set descriptors.
    fd_map = {
        process.stdout.fileno(): ("process", sys.stdout.buffer),
        process.stderr.fileno(): ("error", sys.stderr.buffer),
        sys.stdin.fileno(): ("user", process.stdin),  # Already buffered
    }

    conversation = []

    while True:
        read_fds, _, _ = select.select(list(fd_map.keys()), [], [])
        input_fd = next(fd for fd in read_fds if fd in fd_map)
        role, output_buffer = fd_map[input_fd]

        input_buffer = os.read(input_fd, 1024)
        if input_buffer == b"":
            break
        output_buffer.write(input_buffer)
        output_buffer.flush()
        content = input_buffer.decode("utf-8")
        content = (
            content.replace("\r", "").replace("\n", " ").strip() if content else ""
        )
        conversation.append({"role": role, "content": content})

    process.wait()
    process.stdin.close()
    process.stdout.close()
    process.stderr.close()

    return conversation


def execute_interactive_shell_new(command_line: str) -> list[dict]:
    """Execute a shell command that requires interactivity and return the output

    Args:
        command_line (str): The command line to execute

    Returns:
        list[dict]: The interaction between the user and the process, as a list of dictionaries: [{role: "user"|"process"|"error", content: "the content of the interaction"}, ...]
    """
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_CONSOLE
    else:
        creationflags = 0

    process = subprocess.Popen(
        command_line,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=creationflags,
    )

    # To capture the conversation, we'll read from one set of descriptors, save the output and write it to the other set descriptors.
    fd_map = {
        process.stdout.fileno(): ("process", sys.stdout.buffer),
        process.stderr.fileno(): ("error", sys.stderr.buffer),
        sys.stdin.fileno(): ("user", process.stdin),  # Already buffered
    }

    conversation = []

    WSAStartup = socket.socket().fileno()
    while True:
        read_fds, _, _ = select.select(list(fd_map.keys()), [], [])
        input_fd = next(fd for fd in read_fds if fd in fd_map)
        role, output_buffer = fd_map[input_fd]

        input_buffer = read_input()
        if input_buffer == b"":
            break
        output_buffer.write(input_buffer)
        output_buffer.flush()
        content = input_buffer.decode("utf-8")
        content = (
            content.replace("\r", "").replace("\n", " ").strip() if content else ""
        )
        conversation.append({"role": role, "content": content})

    process.wait()
    process.stdin.close()
    process.stdout.close()
    process.stderr.close()

    return conversation


def ask_user(prompts: list[str]) -> list[str]:
    """
    Ask the user a series of prompts and return the responses

    Args:
        prompts (list[str]): The prompts to ask the user

    Returns:
        list[str]: The responses from the user
    """
    results = []
    for prompt in prompts:
        response = input(prompt)
        results.append(response)
    return results
