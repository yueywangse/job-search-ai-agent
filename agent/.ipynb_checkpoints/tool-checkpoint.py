from abc import ABC, abstractmethod

from agent.state import AgentState


class Tool(ABC):
    """Base class for all agent tools."""
    
    name: str
    description: str
    requires: list[str] = []
    produces: list[str] = []
    
    def can_run(self, state: AgentState) -> bool:
        """Return whether the tool can execute with the current state."""

        return all(
            getattr(state, field) is not None
            for field in self.requires
        )

    @abstractmethod
    def run(self, state: AgentState) -> str:
        """Execute the tool and return a short summary."""