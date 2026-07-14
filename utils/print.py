def print_match(result):
    """Pretty-print the skill matching results."""

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

    print()


def print_analysis(analysis):
    """Pretty-print the match analysis."""

    print("\n========== Analysis ==========\n")

    print("Summary:\n")
    print(analysis.summary)

    print("\nStrengths:\n")
    for item in analysis.strengths:
        print(f"- {item}")

    print("\nGaps:\n")
    for item in analysis.gaps:
        print(f"- {item}")

    print("\nResume Improvements:\n")
    for item in analysis.resume_improvements:
        print(f"- {item}")
        
def get_job_description():
    """Read a multi-line job description from the terminal."""

    print("Paste the job description.")
    print("Press Enter twice when finished.\n")

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    return "\n".join(lines)