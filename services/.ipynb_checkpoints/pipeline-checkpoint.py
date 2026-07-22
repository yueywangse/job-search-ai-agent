from collections.abc import Callable
from pathlib import Path

from agent import ApplicationAgent, AgentState
from builders import CoverLetterBuilder, ResumeBuilder
from config import RESUME_HASH, RESUME_JSON, USE_CACHED_RESUME
from services import LLM
from models import PipelineResult, Resume
from utils import file_hash, load_json, save_json

from .cover_letter_generator import CoverLetterGenerator
from .job_extractor import JobExtractor
from .match_analyzer import MatchAnalyzer
from .resume_extractor import ResumeExtractor
from .resume_parser import ResumeParser
from .resume_tailor import ResumeTailor
from .skill_matcher import SkillMatcher

_RESUME_READ_PROGRESS = 5
_RESUME_EXTRACT_PROGRESS = 15
_DEFAULT_GOAL = "Tailor my resume and generate a cover letter."

class ApplicationPipeline:
    """Run the end-to-end job application pipeline."""
    
    def __init__(self) -> None:
        """Initialize the pipeline services."""
        
        self.llm = LLM()

        self.resume_parser = ResumeParser()
        self.resume_extractor = ResumeExtractor(self.llm)

        self.agent = ApplicationAgent(
            llm=self.llm,
            job_extractor=JobExtractor(self.llm),
            skill_matcher=SkillMatcher(),
            match_analyzer=MatchAnalyzer(self.llm),
            resume_tailor=ResumeTailor(self.llm),
            cover_letter_generator=CoverLetterGenerator(self.llm),
        )

        self.resume_builder = ResumeBuilder()
        self.cover_letter_builder = CoverLetterBuilder()
    
    def create_session(
        self,
        resume: Resume,
        job_text: str
    ) -> AgentState:
        """Create a new application session."""
        
        return AgentState(
            goal=_DEFAULT_GOAL,
            resume=resume,
            job_text=job_text
        )
    
    def chat(
        self,
        state: AgentState,
        message: str,
        progress_callback: Callable[[str, int], None] | None = None
    ) -> PipelineResult:
        """Process a user message and update the application state."""
        
        self.agent.run(
            state=state,
            user_message=message,
            progress_callback=progress_callback
        )

        result = PipelineResult(
            resume=state.resume,
            job=state.job,
            match=state.match,
            analysis=state.analysis,
            tailored_resume=state.tailored_resume,
            cover_letter=state.cover_letter
        )

        self.build_documents(result)

        return result
        
    def load_resume(
        self,
        resume_path: str,
        progress_callback: Callable[[str, int], None] | None = None
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
    
    def _progress(
        self,
        callback: Callable[[str, int], None] | None,
        message: str,
        percent: int
    ) -> None:
        """Update the pipeline progress."""

        if callback:
            callback(message, percent)

    def build_documents(self, result: PipelineResult) -> None:
        """Generate the DOCX resume and cover letter."""

        self.resume_builder.build(result.resume, result.tailored_resume)
        self.cover_letter_builder.build(result.resume, result.cover_letter)