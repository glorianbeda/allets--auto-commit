# AI-Powered Git Commits

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automatically generate your git commit messages using the power of Google's Gemini. This tool integrates directly into your `git commit` workflow, suggesting a clear, conventional commit message based on your staged changes.

## How It Works

This project uses a combination of a local web server and a Git hook to automate commit message generation:

1.  **Local Server**: A Python server using FastAPI runs in the background, providing an endpoint that accepts a `git diff` and returns an AI-generated commit message.
2.  **Git Hook**: A `prepare-commit-msg` hook is installed in your repository. This hook triggers automatically whenever you run `git commit`.
3.  **Workflow**:
    - When you run `git commit`, the hook captures your staged changes (`git diff --cached`).
    - It sends the diff to the local server.
    - The server queries the Google Gemini API to generate a conventional commit message.
    - The hook displays the suggested message and asks for your confirmation (`y/n`).
    - If you approve, it commits directly with the AI message.
    - If you decline, it allows you to write your own message in your default text editor.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system.

### General
- **Python 3.7+**
- **Git**

### Platform-Specific

<details>
<summary><b>Linux (Debian/Ubuntu)</b></summary>

- **curl**: Usually pre-installed.
- **jq**: A command-line JSON processor.
  ```bash
  sudo apt-get update && sudo apt-get install -y jq
  ```

</details>

<details>
<summary><b>macOS</b></summary>

- **Homebrew**: The missing package manager for macOS.
- **jq**:
  ```bash
  brew install jq
  ```

</details>

<details>
<summary><b>Windows</b></summary>

- **Git for Windows**: Provides Git, Git Bash (a terminal for running the scripts), and `curl`. Download it from [git-scm.com](https://git-scm.com/download/win).
- **jq**:
  - **Recommended (via Chocolatey package manager)**:
    ```powershell
    choco install jq
    ```
  - **Manual**: Download the `jq.exe` binary from the [official jq website](https://jqlang.github.io/jq/download/) and place it in a directory that is in your system's PATH.

</details>

---

## Installation

Follow these steps to set up the project.

**1. Clone the Repository**
```bash
git clone https://github.com/glorianbeda/allets--auto-commit.git
cd allets--auto-commit
```

**2. Set Up Python Environment**
It is highly recommended to use a virtual environment.
```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate
# On Windows (using Command Prompt or PowerShell):
.\venv\Scripts\activate
```
Then, install the required Python packages:
```bash
pip install -r requirements.txt
```

**3. Configure Gemini API Key**
You need a Google Gemini API key. You can get one for free from [Google AI Studio](https://aistudio.google.com/app/apikey).

- Create a `.env` file from the example:
  ```bash
  # On Linux/macOS
  cp .env.example .env
  # On Windows
  copy .env.example .env
  ```
- Open the new `.env` file and paste your API key.

**4. Install the Git Hook**
This script will set up the `prepare-commit-msg` hook in your local repository.

- **On Linux/macOS:**
  ```bash
  bash generate.sh
  ```
- **On Windows:**
  You **must** run this command from **Git Bash**, which comes with Git for Windows.
  ```bash
  bash generate.sh
  ```

---

## Usage

To use the tool, you need to have the AI server running in the background.

**1. Start the AI Server**
Open a terminal, navigate to the project directory, and run:
```bash
bash run.sh
```
Keep this terminal open. It will host the local server at `http://localhost:8000`.

**2. Use Git as Usual**
In a **separate terminal**, go about your work.
```bash
# Stage your changes
git add .

# Run the commit command
git commit
```
The hook will now activate, generate a message, and ask for your confirmation.

---

## Troubleshooting

- **Error: `unable to start editor ''` when selecting 'n'**:
  This means you haven't configured a default text editor for Git. The script now warns you about this, but you can fix it permanently with:
  ```bash
  # Example using nano
  git config --global core.editor "nano"

  # Or for Visual Studio Code
  git config --global core.editor "code --wait"
  ```

- **Error: `Failed to get message from AI server`**:
  - Ensure the AI server is running (check the terminal where you ran `bash run.sh`).
  - Verify that your `GEMINI_API_KEY` in the `.env` file is correct.

## Uninstallation

To remove the functionality, simply delete the Git hook file from your repository:

```bash
# On Linux/macOS
rm .git/hooks/prepare-commit-msg

# On Windows
del .git\hooks\prepare-commit-msg
```
You can then stop and close the server terminal.
