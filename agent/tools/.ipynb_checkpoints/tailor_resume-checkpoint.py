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
        
        resume = (
            state.tailored_resume
            if state.tailored_resume is not None
            else state.resume
        )

        state.tailored_resume = self.tailor.tailor(state.resume, state.job, context, state.tailored_resume, state.latest_user_message())
        
        return f"Resume tailored based on user request: {state.latest_user_message()}"