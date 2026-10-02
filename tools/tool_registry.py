class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool):
        """Registers a tool instance."""
        self._tools[tool.name] = tool

    def get_tool(self, name: str):
        return self._tools.get(name)

    def get_all_schemas(self, allowed_tool_names: list = None) -> list:
        """Returns schemas for the AI provider, filtered by allowed names."""
        schemas = []
        for name, tool in self._tools.items():
            if allowed_tool_names is None or name in allowed_tool_names:
                schemas.append(tool.get_schema())
        return schemas

tool_registry = ToolRegistry()
