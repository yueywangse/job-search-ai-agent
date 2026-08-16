from agent.state import AgentState
from agent.tool import Tool
from services.interview_answer_generator import InterviewAnswerGenerator

class GenerateInterviewAnswerTool(Tool):
    """Generate an answer to an interview question."""

    name = "generate_interview_answer"

    description = (
        "Generate a personalized answer to a specific interview "
        "question using the candidate's resume and target job."
    )

    requires = [
        "resume",
        "tailored_resume",
        "job",
        "analysis"
    ]

    produces = ["interview_answer"]

    def __init__(
        self,
        generator: InterviewAnswerGenerator,
    ) -> None:
        self.generator = generator

    def run(self, state: AgentState) -> str:
        """Generate an answer to an interview question."""

        question = state.pending_interview_question

        if question is None:
            raise ValueError("No interview question selected.")

        answer = self.generator.generate(
            state.resume,
            state.tailored_resume,
            state.job,
            state.analysis,
            question
        )

        state.interview_answers[question] = answer

        return "Generated an answer for the interview question."