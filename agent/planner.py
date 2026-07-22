from agent.decision import Decision
from agent.registry import ToolRegistry
from agent.state import AgentState
from services import LLM

class Planner:
    """Plans the next action for the application agent."""

    def __init__(
        self,
        llm: LLM,
        registry: ToolRegistry
    ) -> None:
        self.llm = llm
        self.registry = registry

    def plan(self, state: AgentState) -> Decision:
        """Determine the next tool to execute."""

        return self.llm.generate(
            prompt=self._build_prompt(state),
            schema=Decision
        )

    def _build_prompt(self, state: AgentState) -> str:
        return f"""
You are an AI application agent.

Your responsibility is to decide which tool should execute next.

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
--------------
{state.summary()}

Available Tools
---------------
{self.registry.describe()}

Tool History
------------
{state.tool_history_text()}

Instructions
------------

- Consider the user's latest request in the context of the conversation.
- Use earlier conversation only as context; prioritize the user's latest request.
- Use the application state to determine what information already exists.
- Choose exactly one tool to execute next.
- Do not plan multiple steps ahead.
- Do not skip required intermediate tools.
- Only choose a tool whose prerequisites are already satisfied.
- Never choose a tool that depends on unavailable information.
- Avoid repeating work that has already been completed unless the user's latest request requires it.
- Return "finish" only when no additional tool execution is needed to satisfy the user's latest request.
- Return only a valid Decision object.
- Do not include any additional text.
"""