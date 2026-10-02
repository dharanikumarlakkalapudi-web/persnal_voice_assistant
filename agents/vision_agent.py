from .base_agent import BaseAgent

class VisionAgent(BaseAgent):
    @property
    def agent_id(self) -> str:
        return "vision_agent"

    @property
    def display_name(self) -> str:
        return "Computer Vision Expert"

    @property
    def allowed_tools(self) -> list:
        return [
            "take_screenshot",
            "analyze_screen"
        ]

    @property
    def system_instructions(self) -> str:
        return """
You are JARVIS's specialized Vision Agent.
You excel at interpreting screenshots and visual data on the user's screen.
When asked to see what is on the screen, use take_screenshot followed by analyze_screen.
Provide concise, highly accurate descriptions of visual elements.
"""
