from models import Job
from prompts import JOB_ANALYSIS_PROMPT
from services import LLM


class JobExtractor:
    """Extract structured job information from a job description."""

    def __init__(self, llm: LLM):
        """Initialize the job extractor."""

        self.llm = llm

    def extract(self, job_text: str) -> Job:
        """Extract a structured job description."""

        print(f"Job text length: {len(job_text)} characters")

        prompt = JOB_ANALYSIS_PROMPT.format(job=job_text)

        return self.llm.generate(prompt, schema=Job)
