import yaml
import os

def load_config():
    """Load config.yaml untuk ambil API key dan model name."""
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError("config.yaml tidak ditemukan di folder ai-commit/")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
