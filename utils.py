import json
from pathlib import Path
from match import MatchResult

def save_json(data, filepath: str):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )
        
def get_job_description() -> str:
    print("Paste the job description.")
    print("Press Enter twice when finished.\n")
    lines = []

    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

def print_match(result: MatchResult):
    print("\n========== Match Results ==========\n")
    print(f"Match Score: {result.match_percentage:.1f}%\n")
    print("Matching Skills")
    for skill in result.matching_skills:
        print(f"  ✓ {skill}")
    print("\nMissing Skills")
    for skill in result.missing_skills:
        print(f"  ✗ {skill}")
    print("\nExtra Skills")
    for skill in result.extra_skills:
        print(f"  • {skill}")
        
def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)