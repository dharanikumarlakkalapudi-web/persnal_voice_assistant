from .base_agent import BaseAgent

class ProactiveAgent(BaseAgent):
    @property
    def agent_id(self) -> str:
        return "proactive_agent"

    @property
    def display_name(self) -> str:
        return "Background Monitor"

    @property
    def allowed_tools(self) -> list:
        return [
            "read_email"
            # Note: Screen scraping removed per user request
        ]

    @property
    def system_instructions(self) -> str:
        return """
You are JARVIS's Proactive Background Agent.
You run silently in a separate thread. 
Your job is to periodically check the user's unread emails. 
If you find something highly urgent or important, you should synthesize a short alert message. 
Otherwise, output 'NO_ALERT'.
"""
