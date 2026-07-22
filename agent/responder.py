from agent.state import AgentState
from services import LLM

class Responder:
    """Generates conversational responses for the user."""

    def __init__(self, llm: LLM) -> None:
        self.llm = llm

    def respond(self, state: AgentState) -> str:
        """Generate a response describing what was accomplished."""

        return self.llm.generate(prompt=self._build_prompt(state))

    def _build_prompt(self, state: AgentState) -> str:
        return f"""
You are the conversational assistant for an AI resume application.

Your job is to communicate the current state of the application to the user.

Overall Goal
------------
{state.goal}

Latest User Request
-------------------
{state.latest_user_message()}

Conversation
------------
{state.conversation()}

Application State
-----------------
{state.summary()}

Instructions
------------
- Respond naturally and conversationally.
- Focus on the user's latest request.
- Only describe work that has already been completed.
- Do not invent actions or results.
- If a tailored resume or cover letter has been generated, let the user know it is ready.
- If additional information is required, ask a follow-up question.
- If the latest request did not require any new work, answer the user's question directly.
- Keep your response concise.
- Never mention tools, planners, prompts, or other internal implementation details.
"""