import json
from pathlib import Path
from collections.abc import Callable

from builders import CoverLetterBuilder, ResumeBuilder
from config import RESUME_HASH, RESUME_JSON, USE_CACHED_RESUME
from utils import file_hash, load_json, save_json
from models import PipelineResult, Resume
from .cover_letter_generator import CoverLetterGenerator
from .job_extractor import JobExtractor
from .match_analyzer import MatchAnalyzer
from .resume_extractor import ResumeExtractor
from .resume_parser import ResumeParser
from .resume_tailor import ResumeTailor
from .skill_matcher import SkillMatcher

_RESUME_READ_PROGRESS = 5
_RESUME_EXTRACT_PROGRESS = 15
_JOB_EXTRACT_PROGRESS = 20
_MATCH_PROGRESS = 40
_ANALYSIS_PROGRESS = 60
_TAILOR_PROGRESS = 80
_COVER_LETTER_PROGRESS = 95
_COMPLETE_PROGRESS = 100

class ApplicationPipeline:
    """Run the end-to-end job application pipeline."""

    def __init__(self) -> None:
        """Initialize the pipeline services."""

        self.resume_parser = ResumeParser()
        self.resume_extractor = ResumeExtractor()
        self.job_extractor = JobExtractor()
        self.skill_matcher = SkillMatcher()
        self.match_analyzer = MatchAnalyzer()
        self.resume_tailor = ResumeTailor()
        self.cover_letter_generator = CoverLetterGenerator()

        self.resume_builder = ResumeBuilder()
        self.cover_letter_builder = CoverLetterBuilder()

    def load_resume(
        self,
        resume_path: str,
        progress_callback: Callable[[str, int], None] | None = None,
    ) -> Resume:
        """Load a cached resume or extract a new one."""

        resume_path = Path(resume_path)
        resume_hash = file_hash(resume_path)
        hash_file = Path(RESUME_HASH)
        resume_json = Path(RESUME_JSON)

        use_cache = (
            USE_CACHED_RESUME
            and resume_json.exists()
            and hash_file.exists()
            and hash_file.read_text() == resume_hash
        )

        if use_cache:
            self._progress(progress_callback, "Loading cached resume...", _RESUME_EXTRACT_PROGRESS)

            print("Loading cached resume...")

            return Resume.model_validate(load_json(resume_json))

        self._progress(progress_callback, "Reading resume PDF...", _RESUME_READ_PROGRESS)

        print("Extracting resume...")

        resume_text = self.resume_parser.extract_text(resume_path)
            
        self._progress(progress_callback, "Extracting resume information...", _RESUME_EXTRACT_PROGRESS)

        resume = self.resume_extractor.extract(resume_text)

        save_json(resume.model_dump(), resume_json)

        hash_file.write_text(resume_hash)

        return resume

    def run(
        self,
        resume: Resume,
        job_text: str,
        progress_callback: Callable[[str, int], None] | None = None,
    ) -> PipelineResult:
        """Run the application pipeline."""
            
        self._progress(progress_callback, "Extracting job description...", _JOB_EXTRACT_PROGRESS)

        print("Extracting job...")

        job = self.job_extractor.extract(job_text)
            
        self._progress(progress_callback, "Matching skills...", _MATCH_PROGRESS)

        print("Matching...")

        match = self.skill_matcher.match(resume, job)
            
        self._progress(progress_callback, "Analyzing resume...", _ANALYSIS_PROGRESS)

        print("Analyzing...")

        analysis = self.match_analyzer.analyze(resume, job, match)

        tailor_context = {
            "matching_skills": match.matching_skills,
            "missing_skills": match.missing_skills,
            "summary": analysis.summary,
        }

        tailor_context_json = json.dumps(tailor_context, indent=2)
            
        self._progress(progress_callback, "Tailoring resume...", _TAILOR_PROGRESS)

        print("Tailoring resume...")

        tailored_resume = self.resume_tailor.tailor(resume, job, tailor_context_json)
            
        self._progress(progress_callback, "Generating cover letter...", _COVER_LETTER_PROGRESS)

        print("Generating cover letter...")

        cover_letter = self.cover_letter_generator.generate(resume, tailored_resume, job, tailor_context_json)

        result = PipelineResult(
            resume=resume,
            job=job,
            match=match,
            analysis=analysis,
            tailored_resume=tailored_resume,
            cover_letter=cover_letter,
        )

        self.build_documents(result)
            
        self._progress(progress_callback, "Done!", _COMPLETE_PROGRESS)

        return result
    
    def _progress(
        self,
        callback: Callable[[str, int], None] | None,
        message: str,
        percent: int,
    ) -> None:
        """Update the pipeline progress."""

        if callback:
            callback(message, percent)

    def build_documents(self, result: PipelineResult) -> None:
        """Generate the DOCX resume and cover letter."""

        self.resume_builder.build(result.resume, result.tailored_resume)
        self.cover_letter_builder.build(result.resume, result.cover_letter)