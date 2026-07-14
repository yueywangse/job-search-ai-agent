import json
from pathlib import Path

from builders import CoverLetterBuilder, ResumeBuilder
from config import (
    ANALYSIS_MD,
    ANALYZE_JSON,
    COVER_LETTER_JSON,
    MATCH_JSON,
    RESUME_FILE,
    RESUME_JSON,
    TAILOR_JSON,
    USE_CACHED_RESUME,
)
from models import Resume
from services import (
    CoverLetterGenerator,
    JobExtractor,
    MatchAnalyzer,
    ResumeExtractor,
    ResumeParser,
    ResumeTailor,
    SkillMatcher,
)
from utils import (
    get_job_description,
    load_json,
    print_analysis,
    print_match,
    save_analysis_markdown,
    save_json,
)

parser = ResumeParser()
resume_extractor = ResumeExtractor()
job_extractor = JobExtractor()
matcher = SkillMatcher()
analyzer = MatchAnalyzer()
resume_tailor = ResumeTailor()
resume_builder = ResumeBuilder()
cover_letter_generator = CoverLetterGenerator()
cover_letter_builder = CoverLetterBuilder()

def main() -> None:
    """Run the end-to-end job application pipeline."""

    if USE_CACHED_RESUME and Path(RESUME_JSON).exists():
        print("Loading cached resume...")

        resume = Resume.model_validate(load_json(RESUME_JSON))
    else:
        print("Extracting resume...")

        resume_text = parser.extract_text(RESUME_FILE)
        resume = resume_extractor.extract(resume_text)

        print("Saving resume...")
        save_json(resume.model_dump(), RESUME_JSON)

    print("Getting job description...")
    job_text = get_job_description()

    print("Extracting job...")
    job = job_extractor.extract(job_text)

    print("Matching...")
    result = matcher.match(resume, job)

    print("Saving match...")
    save_json(result.model_dump(), MATCH_JSON)

    print_match(result)

    print("Analyzing...")
    analysis = analyzer.analyze(resume, job, result)

    print("Saving analysis...")
    save_json(analysis.model_dump(), ANALYZE_JSON)

    save_analysis_markdown(analysis, ANALYSIS_MD)

    print_analysis(analysis)

    tailor_context = {
        "matching_skills": result.matching_skills,
        "missing_skills": result.missing_skills,
        "summary": analysis.summary,
    }

    tailor_context_json = json.dumps(tailor_context, indent=2)

    print("Tailoring resume...")
    tailored_resume = resume_tailor.tailor(resume, job, tailor_context_json)

    print("Saving tailored resume...")
    save_json(tailored_resume.model_dump(), TAILOR_JSON)

    print("Building resume...")
    resume_builder.build(resume, tailored_resume)

    print("Generating cover letter...")
    cover_letter = cover_letter_generator.generate(resume, tailored_resume, job, tailor_context_json)

    print("Saving cover letter...")
    save_json(cover_letter.model_dump(), COVER_LETTER_JSON)

    print("Building cover letter...")
    cover_letter_builder.build(resume, cover_letter)

    print("Done!")


if __name__ == "__main__":
    main()