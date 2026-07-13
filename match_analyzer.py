import json

from analysis import MatchAnalysis
from llm import LLM
from prompts import MATCH_ANALYSIS_PROMPT

class MatchAnalyzer:

    def __init__(self):
        self.llm = LLM()

    def analyze(self, resume, job, match) -> MatchAnalysis:
        prompt = MATCH_ANALYSIS_PROMPT.format(
            resume=resume.model_dump_json(indent=2),
            job=job.model_dump_json(indent=2),
            match=match.model_dump_json(indent=2)
        )
        response = self.llm.generate(
            prompt,
            schema=MatchAnalysis
        )

        data = json.loads(response)
        analysis = MatchAnalysis.model_validate(data)

        return analysis