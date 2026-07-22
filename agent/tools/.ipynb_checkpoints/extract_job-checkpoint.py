from agent.state import AgentState
from agent.tool import Tool
from services import JobExtractor

class ExtractJobTool(Tool):
    """Extract structured information from a job description."""

    name = "extract_job"
    description = "Extract structured information from a job description."

    requires = ["job_text"]

    produces = ["job"]

    def __init__(self, extractor: JobExtractor) -> None:
        self.extractor = extractor

    def run(self, state: AgentState) -> str:
        """Extract the job."""

        state.job = self.extractor.extract(state.job_text)
        return (f"Extracted {len(state.job.required_skills)} required skills.")