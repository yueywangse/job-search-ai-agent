from pydantic import BaseModel

class Decision(BaseModel):
    """Represents the planner's next decision."""

    tool: str
    reason: str