from .base_agent import BaseAgent
from configuration.config_manager import config_manager

class GeneralAgent(BaseAgent):
    @property
    def agent_id(self) -> str:
        return "personal_agent"

    @property
    def allowed_tools(self) -> list:
        # In the future, this comes from the database. For now, testing.
        return [
            "get_system_time",
            "execute_powershell",
            "open_application",
            "read_file",
            "create_file",
            "delete_file",
            "take_screenshot",
            "analyze_screen",
            "store_memory",
            "retrieve_memory",
            "read_email",
            "send_email",
            "read_calendar",
            "create_calendar_event"
        ]

    @property
    def system_instructions(self) -> str:
        display_name = config_manager.identity.display_name
        return f"You are {display_name}, a highly intelligent AI assistant. Use the tools provided to answer the user's request concisely."
