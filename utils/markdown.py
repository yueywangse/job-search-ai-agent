import json
from pathlib import Path

def save_analysis_markdown(analysis, path):
    """Save the match analysis as a markdown report."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Resume Match Analysis\n\n")

        f.write("## Summary\n\n")
        f.write(f"{analysis.summary}\n\n")

        f.write("## Strengths\n\n")
        for item in analysis.strengths:
            f.write(f"- {item}\n")

        f.write("\n## Gaps\n\n")
        for item in analysis.gaps:
            f.write(f"- {item}\n")

        f.write("\n## Resume Improvements\n\n")
        for item in analysis.resume_improvements:
            f.write(f"- {item}\n")

        f.write("\n## Interview Risk\n\n")
        for item in analysis.interview_risks:
            f.write(f"- {item}\n")