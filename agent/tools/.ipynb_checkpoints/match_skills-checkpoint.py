from agent.state import AgentState
from agent.tool import Tool
from services import SkillMatcher

class MatchSkillsTool(Tool):
    """Compare the resume against the job."""

    name = "match_skills"
    description = "Compare the resume against the job."

    requires = ["resume", "job"]

    produces = ["match"]

    def __init__(self, matcher: SkillMatcher) -> None:
        self.matcher = matcher

    def run(self, state: AgentState) -> str:
        """Generate a skill match."""

        state.match = self.matcher.match(state.resume, state.job)

        return ("Skilling matching completed")