from abc import ABC, abstractmethod

class BaseTool(ABC):
    """Base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass
        
    @property
    @abstractmethod
    def parameters(self) -> dict:
        """JSON Schema dictionary for the parameters."""
        pass
        
    @property
    @abstractmethod
    def risk_level(self) -> int:
        """Returns the SecurityManager risk level (0-4)."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Executes the tool and returns the result as a string."""
        pass
        
    def get_schema(self) -> dict:
        """Returns the OpenAI/Groq compatible schema dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
