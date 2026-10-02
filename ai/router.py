from .groq_provider import GroqProvider
# from .openai_provider import OpenAIProvider

class AIRouter:
    def get_provider(self, provider_name: str, model: str):
        if provider_name.lower() == "groq":
            return GroqProvider(model=model)
        # elif provider_name.lower() == "openai":
        #     return OpenAIProvider(model=model)
        else:
            raise ValueError(f"Unknown AI Provider: {provider_name}")

ai_router = AIRouter()
