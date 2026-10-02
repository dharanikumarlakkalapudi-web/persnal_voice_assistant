from .general_agent import GeneralAgent
from .coding_agent import CodingAgent
from .vision_agent import VisionAgent
from .proactive_agent import ProactiveAgent

class AgentManager:
    def __init__(self):
        self._agents = {}
        # In the future, this is populated dynamically from SQLite.
        self._register_default_agents()

    def _register_default_agents(self):
        self.register_agent(GeneralAgent())
        self.register_agent(CodingAgent())
        self.register_agent(VisionAgent())
        self.register_agent(ProactiveAgent())

    def register_agent(self, agent):
        self._agents[agent.agent_id] = agent

    def get_agent(self, agent_id: str):
        return self._agents.get(agent_id)

agent_manager = AgentManager()
