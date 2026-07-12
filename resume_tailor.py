import json

from analysis import MatchAnalysis
from job import Job
from llm import LLM
from prompts import RESUME_TAILOR_PROMPT
from resume import Resume
from tailored_resume import TailoredResume

class ResumeTailor:
    def __init__(self):
        self.llm = LLM()

    def tailor(
        self,
        resume: Resume,
        job: Job,
        analysis: str
    ) -> TailoredResume:
        prompt = RESUME_TAILOR_PROMPT.format(
            resume=resume.model_dump_json(indent=2),
            job=job.model_dump_json(indent=2),
            analysis=analysis
        )

        print(f"Prompt length: {len(prompt)} characters")

        response = self.llm.generate(
            prompt,
            schema=TailoredResume
        )
        data = json.loads(response)

        return TailoredResume.model_validate(data)