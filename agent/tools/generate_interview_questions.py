from agent.state import AgentState
from agent.tool import Tool
from services.interview_question_generator import InterviewQuestionGenerator

class GenerateInterviewQuestionsTool(Tool):
    """Generate interview questions."""

    name = "generate_interview_questions"
    description = (
        "Generate technical, behavioral, and role-specific interview "
        "questions for the current job application. Use this tool when "
        "the user explicitly asks for interview questions, interview "
        "preparation, or interview practice."
    )

    requires = [
        "resume",
        "tailored_resume",
        "job",
        "match",
        "analysis"
    ]

    produces = ["interview_questions"]

    def __init__(
        self,
        generator: InterviewQuestionGenerator
    ) -> None:
        self.generator = generator

    def run(self, state: AgentState) -> str:
        """Generate interview questions."""

        state.interview_questions = self.generator.generate(
            state.resume,
            state.tailored_resume,
            state.job,
            state.analysis
        )

        return (
            "Generated technical, behavioral, and role-specific "
            "interview questions."
        )