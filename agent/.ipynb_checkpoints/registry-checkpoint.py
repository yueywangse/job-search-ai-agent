from agent.tool import Tool

class ToolRegistry:
    """Registry of available agent tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool."""

        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        """Return a registered tool."""

        try:
            return self._tools[name]
        except KeyError as exc:
            raise ValueError(f"Unknown tool: '{name}'.") from exc

    def list(self) -> list[Tool]:
        """Return all registered tools."""

        return list(self._tools.values())

    def describe(self) -> str:
        """Return a description of all registered tools."""

        descriptions = []

        for tool in self.list():
            description = [
                tool.name,
                f"Description: {tool.description}",
                "Requires:"
            ]

            if tool.requires:
                description.extend(
                    f"  - {field}"
                    for field in tool.requires
                )
            else:
                description.append("  - None")

            description.append("Produces:")

            if tool.produces:
                description.extend(
                    f"  - {field}"
                    for field in tool.produces
                )
            else:
                description.append("  - None")

            descriptions.append("\n".join(description))

        return "\n\n".join(descriptions)