import subprocess
import google.generativeai as genai
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def get_staged_changes():
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout.strip()

def generate_commit_message(changes):
    config = load_config()
    genai.configure(api_key=config["gemini_api_key"])
    model = genai.GenerativeModel(config.get("model", "gemini-1.5-flash"))

    prompt = f"Generate a short, conventional commit message for these git changes:\n\n{changes}"
    response = model.generate_content(prompt)
    return response.text.strip()

def main():
    changes = get_staged_changes()
    if not changes:
        exit(1)
    message = generate_commit_message(changes)
    print(message)

if __name__ == "__main__":
    main()
