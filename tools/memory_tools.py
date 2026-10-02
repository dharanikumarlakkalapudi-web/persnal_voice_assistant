from .base_tool import BaseTool
from security.security_manager import SecurityManager
from database.sqlite_database import db

class StoreMemoryTool(BaseTool):
    @property
    def name(self) -> str:
        return "store_memory"

    @property
    def description(self) -> str:
        return "Stores a piece of information permanently into JARVIS's memory."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Category of memory (e.g., 'preference', 'fact', 'contact')"},
                "content": {"type": "string", "description": "The information to store"},
                "importance": {"type": "integer", "description": "Importance level 1-5"}
            },
            "required": ["category", "content"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_SAFE

    def execute(self, category: str, content: str, importance: int = 1, **kwargs) -> str:
        db.execute(
            "INSERT INTO memories (category, content, importance, source) VALUES (?, ?, ?, 'llm')",
            (category, content, importance)
        )
        return f"Memory stored successfully in category '{category}'."

class RetrieveMemoryTool(BaseTool):
    @property
    def name(self) -> str:
        return "retrieve_memory"

    @property
    def description(self) -> str:
        return "Searches JARVIS's permanent memory for stored information."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "search_query": {"type": "string", "description": "Text to search for in memories"}
            },
            "required": ["search_query"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_SAFE

    def execute(self, search_query: str, **kwargs) -> str:
        query = f"%{search_query}%"
        results = db.fetchall("SELECT category, content, created_at FROM memories WHERE content LIKE ?", (query,))
        
        if not results:
            return f"No memories found matching '{search_query}'."
            
        formatted_results = [f"[{r['category']} - {r['created_at']}]: {r['content']}" for r in results]
        return "Found memories:\n" + "\n".join(formatted_results)
