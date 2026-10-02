from configuration.manager import config_manager
from ai.groq_provider import GroqProvider
from ai.openai_provider import OpenAIProvider

class ProviderManager:
    """Manages AI providers and model routing."""
    
    def __init__(self):
        self.providers = {}
        # In the future we will initialize all supported providers here
        self.register_provider("groq", GroqProvider())
        self.register_provider("openai", OpenAIProvider())

    def register_provider(self, provider_id: str, provider_instance):
        self.providers[provider_id] = provider_instance

    def get_default_provider(self):
        provider_id = config_manager.get("ai_providers.default", "groq")
        if provider_id not in self.providers:
            return self.providers.get("groq") # Fallback
        return self.providers[provider_id]

    def get_default_model(self) -> str:
        provider_id = config_manager.get("ai_providers.default", "groq")
        return config_manager.get(f"ai_providers.models.{provider_id}", "openai/gpt-oss-20b")

provider_manager = ProviderManager()
