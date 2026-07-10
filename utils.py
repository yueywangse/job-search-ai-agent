import json
from pathlib import Path

def save_json(data, filename: str):
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)