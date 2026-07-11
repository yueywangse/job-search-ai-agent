from resume_extractor import ResumeExtractor
from resume_parser import ResumeParser
from job_extractor import JobExtractor
from skill_matcher import SkillMatcher
from utils import save_json, get_job_description, print_match, print_analysis
from config import RESUME_FILE, RESUME_JSON, MATCH_JSON, USE_CACHED_RESUME, ANALYZE_JSON
from pathlib import Path
from resume import Resume
from utils import load_json
from match_analyzer import MatchAnalyzer

parser = ResumeParser()
resume_extractor = ResumeExtractor()
job_extractor = JobExtractor()
matcher = SkillMatcher()
analyzer = MatchAnalyzer()

def main():
    if USE_CACHED_RESUME and Path(RESUME_JSON).exists():
        print("Loading cached resume...")

        resume = Resume.model_validate(
            load_json(RESUME_JSON)
        )
    else:
        print("Extracting resume...")

        resume_text = parser.extract_text(RESUME_FILE)
        resume = resume_extractor.extract(resume_text)
        save_json(
            resume.model_dump(),
            RESUME_JSON
        )

    print("Resume analyzed successfully!")
    print("Saved to outputs/resume.json")
    
    print("Getting job description...")
    job_text = get_job_description()
    
    print("Extracting job...")
    job = job_extractor.extract(job_text)
    
    print("Matching...")
    result = matcher.match(
        resume,
        job
    )
    
    print("Saving...")
    save_json(
        result.model_dump(),
        MATCH_JSON
    )
    
    print_match(result)
    
    print("Analyzing")
    analysis = analyzer.analyze(
        resume,
        job,
        result
    )
    
    print("Saving...")
    save_json(
        analysis.model_dump(),
        ANALYZE_JSON
    )
    
    print("Done!")

    print_analysis(analysis)

if __name__ == "__main__":
    main()