"""Execute interactive shell commands in the workspace"""
from calendar import c
import os
import subprocess
import sys


def execute_interactive_shell_linux(command_line: str) -> list[dict]:
    """Execute a shell command that requires interactivity and return the output.

    Args:
        command_line (str): The command line to execute

    Returns:
        list[dict]: The interaction between the user and the process, as a list of dictionaries: [{role: "user"|"process"|"error", content: "the content of the interaction"}, ...]
    """
    import select

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


def execute_interactive_shell_crossplatform(command_line: str) -> list[dict]:
    """Execute a shell command that requires interactivity and return the output.
    This can also work on linux, but is less native than the other function.

    Args:
        command_line (str): The command line to execute

    Returns:
        list[dict]: The interaction between the user and the process, as a list of dictionaries: [{role: "user"|"process"|"error", content: "the content of the interaction"}, ...]
    """
    from sarge import Capture, Command

    command = Command(
        command_line,
        stdout=Capture(buffer_size=1),
        stderr=Capture(buffer_size=1),
    )
    command.run(input=subprocess.PIPE, async_=True)

    # To capture the conversation, we'll read from one set of descriptors, save the output and write it to the other set descriptors.
    fd_map = {
        command.stdout: ("process", sys.stdout.buffer),
        command.stderr: ("error", sys.stderr.buffer),
    }

    conversation = []

    while True:
        output = {fd: fd.read(timeout=0.1) for fd in fd_map.keys()}
        if not any(output.values()):
            break

        content = ""
        for fd, output_content in output.items():
            if output_content:
                output_content = (
                    output_content + b"\n"
                    if not output_content.endswith(b"\n")
                    else output_content
                )
                fd_map[fd][1].write(output_content)
                fd_map[fd][1].flush()

                content = output_content.decode("utf-8")
                content = (
                    content.replace("\r", "").replace("\n", " ").strip()
                    if content
                    else ""
                )
                conversation.append({"role": fd_map[fd][0], "content": content})

        if any(output.values()):
            prompt = "Response [None]: "
            os.write(sys.stdout.fileno(), prompt.encode("utf-8"))
            stdin = os.read(sys.stdin.fileno(), 1024)
            if stdin != b"":
                try:
                    command.stdin.write(stdin)
                    command.stdin.flush()
                    content = stdin.decode("utf-8")
                    content = (
                        content.replace("\r", "").replace("\n", " ").strip()
                        if content
                        else ""
                    )
                    conversation.append({"role": "user", "content": content})
                except (BrokenPipeError, OSError):
                    # Child process already exited
                    print("Command exited... returning.")

    command.wait()
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


def execute_interactive_shell(command_line: str) -> list[dict]:
    """Execute a shell command that requires interactivity and return the output.

    Args:
        command_line (str): The command line to execute

    Returns:
        list[dict]: The interaction between the user and the process, as a list of dictionaries: [{role: "user"|"process"|"error", content: "the content of the interaction"}, ...]
    """
    if sys.platform == "win32":
        return execute_interactive_shell_crossplatform(command_line)
    else:
        return execute_interactive_shell_linux(command_line)
