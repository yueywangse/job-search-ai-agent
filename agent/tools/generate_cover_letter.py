import json

from agent.state import AgentState
from agent.tool import Tool
from services import CoverLetterGenerator

class GenerateCoverLetterTool(Tool):
    """Generate a cover letter."""

    name = "generate_cover_letter"
    description = "Generate a cover letter."

    requires = [
        "resume",
        "tailored_resume",
        "job",
        "match",
        "analysis",
    ]

    produces = ["cover_letter"]

    def __init__(self, generator: CoverLetterGenerator) -> None:
        self.generator = generator

    def run(self, state: AgentState) -> str:
        """Generate a cover letter."""

        context = state.tailor_context()
        state.cover_letter = self.generator.generate(state.resume, state.tailored_resume, state.job, context, state.cover_letter, state.latest_user_message())
        
        return (
            f"Generated a cover letter in response to the user's request "
            f"'{state.latest_user_message()}'."
        )