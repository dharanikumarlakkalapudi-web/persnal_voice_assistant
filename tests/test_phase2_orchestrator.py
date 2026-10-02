import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.application import get_app
from core.agent_orchestrator import AgentOrchestrator
from tools.tool_registry import tool_registry
from tools.os_tools import GetSystemTimeTool

def run_tests():
    print("=== JARVIS V2 Phase 2: Core Agent Test ===\n")
    
    # 1. Boot Foundation
    app = get_app()
    
    # 2. Register Tool
    time_tool = GetSystemTimeTool()
    tool_registry.register(time_tool)
    print(f"Registered Tool: {time_tool.name}")
    
    # 3. Create Orchestrator
    orchestrator = AgentOrchestrator(verbose=True)
    
    # 4. Test Query
    query = "What time is it right now? Please answer in a friendly way."
    print(f"\nUser Query: \"{query}\"")
    
    response = orchestrator.process_request(query)
    
    print("\n[FINAL OUTPUT TO USER]")
    print(response.encode('ascii', 'ignore').decode())
    print("\n=== TEST COMPLETED ===")

if __name__ == "__main__":
    run_tests()
