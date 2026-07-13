import json

from job import Job
from llm import LLM
from cover_letter import CoverLetter
from prompts import COVER_LETTER_PROMPT
from resume import Resume
from tailored_resume import TailoredResume

class CoverLetterGenerator:

    def __init__(self):
        self.llm = LLM()

    def generate(self, resume: Resume, tailored_resume: TailoredResume, job: Job, analysis: str) -> CoverLetter:
        prompt = COVER_LETTER_PROMPT.format(
            resume=resume.model_dump_json(indent=2),
            tailored_resume=tailored_resume.model_dump_json(indent=2),
            job=job.model_dump_json(indent=2),
            analysis=analysis
        )

        print(f"Prompt length: {len(prompt)} characters")

        response = self.llm.generate(
            prompt,
            schema=CoverLetter
        )

        data = json.loads(response)

        return CoverLetter.model_validate(data)