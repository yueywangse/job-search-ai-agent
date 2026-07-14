from config import (
    ANALYSIS_MD,
    ANALYZE_JSON,
    COVER_LETTER_JSON,
    MATCH_JSON,
    RESUME_FILE,
    TAILOR_JSON,
)
from services import ApplicationPipeline
from utils import (
    get_job_description,
    save_analysis_markdown,
    save_json,
)

pipeline = ApplicationPipeline()


def main() -> None:
    """Run the end-to-end job application pipeline."""

    try:
        resume = pipeline.load_resume(RESUME_FILE)

        print("Loading job description...")

        job_text = get_job_description()

        result = pipeline.run(resume, job_text)

        print("Saving match...")
        save_json(result.match.model_dump(), MATCH_JSON)

        print("Saving analysis...")
        save_json(result.analysis.model_dump(), ANALYZE_JSON)
        save_analysis_markdown(result.analysis, ANALYSIS_MD)

        print("Saving tailored resume...")
        save_json(result.tailored_resume.model_dump(), TAILOR_JSON)

        print("Saving cover letter...")
        save_json(result.cover_letter.model_dump(), COVER_LETTER_JSON)

        print("Done!")

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()