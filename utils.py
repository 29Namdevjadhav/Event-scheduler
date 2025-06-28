import json
import os

def load_events(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)

def save_events(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
