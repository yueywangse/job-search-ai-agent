import json

from llm import LLM
from resume import Resume
from prompts import RESUME_ANALYSIS_PROMPT


class ResumeExtractor:
    def __init__(self):
        self.llm = LLM()

    def extract(self, resume_text: str) -> Resume:
        prompt = RESUME_ANALYSIS_PROMPT.format(
            resume=resume_text
        )
        response = self.llm.generate(
            prompt,
            schema=Resume
        )

        data = json.loads(response)
        
        return Resume.model_validate(data)