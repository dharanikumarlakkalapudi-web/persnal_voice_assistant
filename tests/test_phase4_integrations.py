import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.application import get_app
from core.agent_orchestrator import AgentOrchestrator
from tools.tool_registry import tool_registry
from tools.email_tools import ReadEmailTool, SendEmailTool
from tools.calendar_tools import ReadCalendarTool, CreateCalendarEventTool

def run_tests():
    print("=== JARVIS V2 Phase 4: Integrations Test ===\n")
    
    app = get_app()
    
    # Register integration tools
    tool_registry.register(ReadEmailTool())
    tool_registry.register(SendEmailTool())
    tool_registry.register(ReadCalendarTool())
    tool_registry.register(CreateCalendarEventTool())
    
    # Mock integrations to avoid OAuth browser popup during automated tests
    from integrations.gmail.gmail_service import gmail_service
    gmail_service.read_unread_emails = lambda **kwargs: "Inbox: test@example.com\nEmail 1:\nFrom: test@example.com\nSubject: Test\nSnippet: This is a mocked email for testing.\n"

    orchestrator = AgentOrchestrator(verbose=True)
    
    print("\n[SCENARIO] Safe Integration Execution (ReadEmail)")
    query = "Please read my latest 2 unread emails from all accounts."
    print(f"\nUser Query: \"{query}\"")
    
    response = orchestrator.process_request(query)
    
    print("\n[OUTPUT]")
    print(response.encode('ascii', 'ignore').decode())
    print("\n=== TEST COMPLETED ===")

if __name__ == "__main__":
    run_tests()
