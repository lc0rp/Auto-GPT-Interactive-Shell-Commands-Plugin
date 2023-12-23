# Auto-GPT Interactive Shell Commands Plugin

## <u>Overview</u>

This plugin allows Auto-GPT to execute interactive shell commands and get feedback from the user.

# Status - Deprecated

These features or similar ones are now available in Auto-GPT. This repo will be archived soon. 


## <u>Commands</u>

1. **ask_user**: 
    - With this command, Auto-GPT can ask the user questions. The command takes a list of questions, and an optional timeout, and returns a list of answers.
2. **execute_interactive_shell**:
    - Enables Auto-GPT to execute shell commands, with interactivity. It takes a command, and optional timeout, and returns the interactions between the user and the process, as a list of dictionaries: [{role: "user"|"process"|"error", content: "the content of the interaction"}, ...]

## <u>Timeout Configuration</u>

Add the following settings to your .env file to customize the plugin timeout:

- INTERACTIVE_SHELL_TIMEOUT_SECONDS: This setting allows you to adjust the timeout for the sub-process, which is set to 15 minutes by default.

Note that Auto-GPT can change the timeout when it invokes the command.

## Installation

Download this repository as a .zip file, copy it to ./plugins/, and rename it to Auto-GPT-Interactive-Shell-Commands-Plugin.zip.

To download it directly from your Auto-GPT directory, you can run this command on Linux or MacOS:

```
curl -o ./plugins/Auto-GPT-Interactive-Shell-Commands-Plugin.zip https://github.com/lc0rp/Auto-GPT-Interactive-Shell-Commands-Plugin/archive/refs/heads/master.zip
```

In PowerShell:

```
Invoke-WebRequest -Uri "https://github.com/lc0rp/Auto-GPT-Interactive-Shell-Commands-Plugin/archive/refs/heads/master.zip" -OutFile "./plugins/Auto-GPT-Interactive-Shell-Commands-Plugin.zip"
```

## Help and discussion:

Discord: https://discord.com/channels/1092243196446249134/1109480174321414214"