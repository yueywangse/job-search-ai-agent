from agent.state import AgentState
from agent.tool import Tool
from services import MatchAnalyzer

class AnalyzeResumeTool(Tool):
    """Analyze the resume."""

    name = "analyze_resume"
    description = "Analyze the resume."

    requires = ["resume", "job", "match"]

    produces = ["analysis"]

    def __init__(self, analyzer: MatchAnalyzer) -> None:
        self.analyzer = analyzer

    def run(self, state: AgentState) -> str:
        """Analyze the resume."""

        state.analysis = self.analyzer.analyze(state.resume, state.job, state.match)
        return ("Resume Analyzed")