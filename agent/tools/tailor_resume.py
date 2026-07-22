import json

from agent.state import AgentState
from agent.tool import Tool
from services import ResumeTailor

class TailorResumeTool(Tool):
    """Tailor the resume."""

    name = "tailor_resume"
    description = "Tailor the resume for the job."

    requires = ["resume", "job", "match", "analysis"]

    produces = ["tailored_resume"]

    def __init__(self, tailor: ResumeTailor) -> None:
        self.tailor = tailor

    def run(self, state: AgentState) -> str:
        """Tailor the resume."""

        context = state.tailor_context()

        state.tailored_resume = self.tailor.tailor(state.resume, state.job, context)
        
        return("Resume Tailored")