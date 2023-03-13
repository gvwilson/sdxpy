import os
from pathlib import Path
import yaml

ENV_VAR = "MCCOLE_CONFIG"
HOME = "HOME"
CONFIG_FILE = ".mccole"

def load_config(filename):
    return _load_system() | load_user() | _load_file(filename)

def _load_system():
    var = os.getenv(ENV_VAR)
    return _load_file(var) if var else {}

def _load_user():
    home = os.getenv(HOME)
    if not home:
        return {}
    filename = Path(home, CONFIG_FILE)
    if not filename.exists():
        return {}
    return _load_file(filename)

def _load_file(filename):
    with open(filename, "r") as reader:
        return yaml.safe_load(reader)
