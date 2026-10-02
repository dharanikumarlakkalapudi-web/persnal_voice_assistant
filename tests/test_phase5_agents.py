import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.application import get_app
from core.agent_orchestrator import AgentOrchestrator
from tools.tool_registry import tool_registry

# Import tools for registry
from tools.os_tools import ExecutePowerShellTool
from tools.email_tools import ReadEmailTool

# Mock integration for test
from integrations.gmail.gmail_service import gmail_service
gmail_service.read_unread_emails = lambda **kwargs: "Inbox: test@example.com\nEmail 1:\nFrom: test@example.com\nSubject: URGENT: Server Down\nSnippet: The main database is down! Please fix immediately!\n"

import face_tools
face_tools.verify_user_face = lambda: True

def run_tests():
    print("=== JARVIS V2 Phase 5: Multi-Agent Routing Test ===\n")
    
    app = get_app()
    
    tool_registry.register(ExecutePowerShellTool())
    tool_registry.register(ReadEmailTool())
    
    orchestrator = AgentOrchestrator(verbose=True)
    
    print("\n[SCENARIO 1] Coding Agent Routing")
    query1 = "Write a python script that prints 'Hello Multi-Agent World' and execute it using powershell."
    print(f"\nUser Query: \"{query1}\"")
    
    response1 = orchestrator.process_request(query1)
    
    print("\n[OUTPUT]")
    print(response1.encode('ascii', 'ignore').decode())

    print("\n-------------------------------------------------\n")

    print("[SCENARIO 2] Proactive Agent Routing (Simulating Background Worker)")
    query2 = "[HINT: Route to proactive_agent] System Request: Check unread emails. If there is anything highly urgent, summarize it as an alert. Otherwise, respond exactly with 'NO_ALERT'."
    print(f"\nSystem Query: \"{query2}\"")
    
    response2 = orchestrator.process_request(query2)
    
    print("\n[OUTPUT]")
    print(response2.encode('ascii', 'ignore').decode())
    
    print("\n=== TEST COMPLETED ===")

if __name__ == "__main__":
    run_tests()
