import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.application import get_app
from core.agent_orchestrator import AgentOrchestrator
from tools.tool_registry import tool_registry
from tools.os_tools import ExecutePowerShellTool
from tools.filesystem_tools import ReadFileTool

def run_tests():
    print("=== JARVIS V2 Phase 3: Face ID & Security Test ===\n")
    
    app = get_app()
    
    tool_registry.register(ExecutePowerShellTool())
    tool_registry.register(ReadFileTool())
    
    orchestrator = AgentOrchestrator(verbose=True)
    
    print("\n[SCENARIO 1] Safe Tool Execution (ReadFile)")
    # Using read_file on schema.sql
    query1 = f"Please read the contents of {os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')} and tell me what the first table is."
    print(f"\nUser Query: \"{query1}\"")
    response1 = orchestrator.process_request(query1)
    print("\n[OUTPUT]")
    print(response1.encode('ascii', 'ignore').decode())

    print("\n-------------------------------------------------\n")

    print("[SCENARIO 2] Dangerous Tool Execution (PowerShell with Face ID)")
    query2 = "Run a powershell command to echo 'FACE ID TEST SUCCESSFUL'."
    print(f"\nUser Query: \"{query2}\"")
    response2 = orchestrator.process_request(query2)
    print("\n[OUTPUT]")
    print(response2.encode('ascii', 'ignore').decode())
    
    print("\n=== TEST COMPLETED ===")

if __name__ == "__main__":
    run_tests()
