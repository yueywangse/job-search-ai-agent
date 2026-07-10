import json

from llm import LLM
from job import Job
from prompts import JOB_ANALYSIS_PROMPT


class JobExtractor:
    def __init__(self):
        self.llm = LLM()

    def extract(self, job_text: str) -> Job:
        print(f"Job text length: {len(job_text)} characters")
        prompt = JOB_ANALYSIS_PROMPT.format(
            job=job_text
        )
        response = self.llm.generate(
            prompt,
            schema=Job
        )

        data = json.loads(response)
        
        return Job.model_validate(data)