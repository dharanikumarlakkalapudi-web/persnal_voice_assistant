from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @property
    @abstractmethod
    def agent_id(self) -> str:
        pass

    @property
    @abstractmethod
    def allowed_tools(self) -> list:
        """List of tool names this agent is allowed to use."""
        pass

    @property
    @abstractmethod
    def system_instructions(self) -> str:
        """The base system prompt for this agent."""
        pass
