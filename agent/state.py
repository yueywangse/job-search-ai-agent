import json
from pydantic import BaseModel, Field
from typing import Literal

from models import (
    MatchAnalysis,
    CoverLetter,
    Job,
    Resume,
    MatchResult,
)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    
class ToolExecution(BaseModel):
    tool: str
    reason: str
    result: str

class AgentState(BaseModel):
    """Represents the current state of the application agent."""
    
    goal: str

    messages: list[ChatMessage] = Field(default_factory=list)

    resume: Resume
    job_text: str

    job: Job | None = None
    match: MatchResult | None = None
    analysis: MatchAnalysis | None = None
    tailored_resume: Resume | None = None
    cover_letter: CoverLetter | None = None
    
    completed_tools: list[str] = Field(default_factory=list)
    tool_history: list[ToolExecution] = Field(default_factory=list)
    
    def tailor_context(self) -> str:
        """Return the tailoring context."""

        if self.match is None or self.analysis is None:
            raise ValueError(
                "Tailor context requires both match and analysis."
            )

        return json.dumps(
            {
                "matching_skills": self.match.matching_skills,
                "missing_skills": self.match.missing_skills,
                "summary": self.analysis.summary
            },
            indent=2
        )
    
    def add_user_message(self, content: str) -> None:
        """Append a user message to the conversation."""
        
        self.messages.append(ChatMessage(role="user", content=content))
        
    def add_assistant_message(self, content: str) -> None:
        """Append an assistant message to the conversation."""
        
        self.messages.append(ChatMessage(role="assistant", content=content))
        
    def conversation(self, limit: int = 10) -> str:
        """Return the conversation as formatted text."""
        
        messages = self.messages[-limit:]
        return "\n\n".join(
            f"{m.role.title()}: {m.content}"
            for m in messages
        )
    
    def summary(self) -> str:
        """Return a summary of the current application state."""
        
        return (
            f"Job Extracted: {'Yes' if self.job else 'No'}\n"
            f"Skill Match: {'Yes' if self.match else 'No'}\n"
            f"Resume Analysis: {'Yes' if self.analysis else 'No'}\n"
            f"Resume Tailored: {'Yes' if self.tailored_resume else 'No'}\n"
            f"Cover Letter Generated: {'Yes' if self.cover_letter else 'No'}\n\n"
            f"Completed Tools:\n"
            f"{', '.join(self.completed_tools) or 'None'}\n\n"
            f"Recent Tool Results:\n"
            f"{self.tool_history_text()}"
        )
    
    def complete_tool(self, tool_name: str) -> None:
        """Mark a tool as completed."""
        
        if tool_name not in self.completed_tools:
            self.completed_tools.append(tool_name)
        
    def add_tool_execution(
        self,
        tool: str,
        reason: str,
        result: str
    ) -> None:
        """Record a completed tool execution."""

        self.tool_history.append(
            ToolExecution(
                tool=tool,
                reason=reason,
                result=result,
            )
        )
        
    def tool_history_text(self, limit: int = 5) -> str:
        """Return recent tool executions as formatted text."""
        
        if not self.tool_history:
            return "None"

        history = self.tool_history[-limit:]
        
        return "\n".join(
            f"- {execution.tool}\n"
            f"  Reason: {execution.reason}\n"
            f"  Result: {execution.result}"
            for execution in history
        )
    
    def latest_user_message(self) -> str | None:
        """Return the most recent user message."""

        for message in reversed(self.messages):
            if message.role == "user":
                return message.content

        return None