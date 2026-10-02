from .base_agent import BaseAgent

class CodingAgent(BaseAgent):
    @property
    def agent_id(self) -> str:
        return "coding_agent"

    @property
    def display_name(self) -> str:
        return "Software Engineer"

    @property
    def allowed_tools(self) -> list:
        return [
            "read_file",
            "create_file",
            "delete_file",
            "execute_powershell"
            # Note: A pure execute_python tool could be added later, 
            # but for now execute_powershell can run python scripts.
        ]

    @property
    def system_instructions(self) -> str:
        return """
You are JARVIS's specialized Coding Agent, an expert software developer.
Your goal is to write clean, secure, and bug-free code.
You have access to filesystem tools and PowerShell execution.
When executing PowerShell to run Python scripts or tests, ensure you handle paths correctly.
Avoid writing code with hardcoded credentials. Always use environment variables or configuration files.
"""
