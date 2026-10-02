from .base_tool import BaseTool
from security.security_manager import SecurityManager
from integrations.gmail.gmail_service import gmail_service

class ReadEmailTool(BaseTool):
    @property
    def name(self) -> str:
        return "read_email"

    @property
    def description(self) -> str:
        return "Reads unread emails from the user's Gmail accounts."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer", 
                    "description": "Number of emails to read (default 3)"
                },
                "account_name": {
                    "type": "string",
                    "description": "Specific account to read from (e.g. 'college', 'personal'). Default is 'all'."
                }
            }
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_SAFE

    def execute(self, max_results: int = 3, account_name: str = "all", **kwargs) -> str:
        return gmail_service.read_unread_emails(max_results=max_results, account_name=account_name)

class SendEmailTool(BaseTool):
    @property
    def name(self) -> str:
        return "send_email"

    @property
    def description(self) -> str:
        return "Sends an email. DANGEROUS."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email address"},
                "subject": {"type": "string", "description": "Email subject"},
                "body": {"type": "string", "description": "Email body content"}
            },
            "required": ["to", "subject", "body"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_DANGEROUS  # Level 3: Requires Face ID

    def execute(self, to: str, subject: str, body: str, **kwargs) -> str:
        # Stub for Phase 4. Would normally use gmail_service.send_email()
        return f"Securely sent email to {to} with subject '{subject}'. (Stub)"
