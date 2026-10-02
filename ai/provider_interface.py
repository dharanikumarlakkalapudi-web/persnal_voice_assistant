from abc import ABC, abstractmethod

class AIProvider(ABC):
    """Base interface for all AI models (Groq, OpenAI, Ollama, etc.)"""
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: str = None, tools: list = None) -> dict:
        """
        Sends a prompt to the LLM and returns a dictionary containing:
        - "text": The textual response (if any)
        - "tool_calls": A list of dictionaries representing requested tool calls
            - "id": Tool call ID
            - "name": Function name
            - "arguments": JSON string or dict of arguments
        """
        pass
