import os
from .base_tool import BaseTool
from security.security_manager import SecurityManager

class ReadFileTool(BaseTool):
    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Reads the contents of a file."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Absolute path to the file"}
            },
            "required": ["filepath"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_SAFE

    def execute(self, filepath: str, **kwargs) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"File contents:\n{content[:2000]}" # Limit size to avoid overwhelming context
        except Exception as e:
            return f"Failed to read file: {str(e)}"

class CreateFileTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_file"

    @property
    def description(self) -> str:
        return "Creates a new file with the specified content."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Absolute path to create the file at"},
                "content": {"type": "string", "description": "Content to write into the file"}
            },
            "required": ["filepath", "content"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_LOW

    def execute(self, filepath: str, content: str, **kwargs) -> str:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully created file at {filepath}"
        except Exception as e:
            return f"Failed to create file: {str(e)}"

class DeleteFileTool(BaseTool):
    @property
    def name(self) -> str:
        return "delete_file"

    @property
    def description(self) -> str:
        return "Deletes a file permanently. DANGEROUS."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Absolute path to the file to delete"}
            },
            "required": ["filepath"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_DANGEROUS # Level 3: Needs Face ID

    def execute(self, filepath: str, **kwargs) -> str:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return f"Successfully deleted {filepath}"
            else:
                return f"File not found: {filepath}"
        except Exception as e:
            return f"Failed to delete file: {str(e)}"
