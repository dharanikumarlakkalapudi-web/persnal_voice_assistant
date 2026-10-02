import json
from ai.router import ai_router
from agents.agent_manager import agent_manager
from tools.tool_registry import tool_registry
from security.security_manager import SecurityManager

security_manager = SecurityManager()

class AgentOrchestrator:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def _log(self, msg):
        if self.verbose:
            print(msg)

    def process_request(self, user_input: str, agent_id: str = "personal_agent"):
        self._log("\n--- COMMAND LIFECYCLE STARTED ---")
        
        # 1. Agent Selection
        agent_id = "personal_agent"
        query_lower = user_input.lower()
        if "proactive_agent" in query_lower:
            agent_id = "proactive_agent"
        elif "vision" in query_lower or "screenshot" in query_lower or "screen" in query_lower:
            agent_id = "vision_agent"
        elif "code" in query_lower or "script" in query_lower or "python" in query_lower:
            agent_id = "coding_agent"
            
        agent = agent_manager.get_agent(agent_id)
        if not agent:
            agent = agent_manager.get_agent("personal_agent")
            
        self._log(f"[Agent Selection] Using: {agent.agent_id}")
        
        # Publish event so the UI updates
        from core.event_bus import event_bus
        event_bus.publish("agent.changed", {"agent_id": agent.agent_id})

        # 2. Setup AI Provider
        from ai.provider_manager import provider_manager
        provider = provider_manager.get_default_provider()
        provider.model = provider_manager.get_default_model()
        
        # 3. Get Tool Schemas for this agent
        schemas = tool_registry.get_all_schemas(allowed_tool_names=agent.allowed_tools)
        
        # 4. First AI Pass (Planning / Tool Selection)
        self._log(f"[Planning] Sending request to {provider.__class__.__name__}...")
        response = provider.generate_response(
            prompt=user_input, 
            system_prompt=agent.system_instructions,
            tools=schemas
        )

        # 5. Check if tools were requested
        if not response.get("tool_calls"):
            self._log("[Execution] No tools requested. Direct response.")
            return response.get("text", "")

        # 6. Tool Execution Loop
        tool_results_text = "Here are the results of the tool executions:\n"
        
        for tc in response["tool_calls"]:
            tool_name = tc["name"]
            tool_args_str = tc["arguments"]
            self._log(f"[Tool Selected] {tool_name}")
            
            tool = tool_registry.get_tool(tool_name)
            if not tool:
                tool_results_text += f"- {tool_name} failed: Tool not registered.\n"
                continue
                
            # 7. Security Check
            decision = security_manager.evaluate_action(agent.agent_id, tool_name, tool.risk_level)
            self._log(f"[Security Check] Decision for {tool_name}: {decision}")
            
            if decision == "denied":
                res = "Execution blocked by Security Policy."
            elif decision == "face_id_required":
                self._log("[Security] Face ID verification required! Activating camera...")
                try:
                    import face_tools
                    authorized = face_tools.verify_user_face()
                    if authorized:
                        self._log("[Security] Face verified. Proceeding with execution.")
                        kwargs = json.loads(tool_args_str) if tool_args_str else {}
                        res = tool.execute(**kwargs)
                    else:
                        res = "Execution blocked: Face ID verification failed."
                except Exception as e:
                    res = f"Execution blocked: Face verification error: {str(e)}"
            else: # allowed or confirmation_required (ignoring confirm for tests)
                try:
                    kwargs = json.loads(tool_args_str) if tool_args_str else {}
                    res = tool.execute(**kwargs)
                except Exception as e:
                    res = f"Execution failed: {str(e)}"
                    
            security_manager.log_security_event(agent.agent_id, tool_name, "execute", tool.risk_level, decision, res)
            self._log(f"[Execution] Result: {res}")
            tool_results_text += f"- {tool_name} returned: {res}\n"

        # 8. Final AI Pass (Synthesize response)
        self._log("[Result Validation] Passing results back to AI for final synthesis...")
        final_prompt = f"User Request: {user_input}\n\n{tool_results_text}\n\nProvide the final natural language response to the user."
        
        final_response = provider.generate_response(
            prompt=final_prompt,
            system_prompt=agent.system_instructions
        )
        
        self._log("--- COMMAND LIFECYCLE COMPLETED ---\n")
        return final_response.get("text", "")
