import os
from openai import OpenAI
from .provider_interface import AIProvider
from security.credential_vault import vault

class OpenAIProvider(AIProvider):
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.client = None

    def _get_client(self):
        if self.client:
            return self.client
            
        api_key = vault.get_credential("openai_api_key")
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
            
        if not api_key:
            raise ValueError("[OpenAIProvider] API Key not found in Vault or Environment!")
            
        self.client = OpenAI(api_key=api_key)
        return self.client

    def generate_response(self, prompt: str, system_prompt: str = None, tools: list = None) -> dict:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        messages.append({"role": "user", "content": prompt})

        # Format tools for OpenAI function calling standard
        formatted_tools = None
        if tools:
            formatted_tools = [{"type": "function", "function": t} for t in tools]

        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=formatted_tools,
            temperature=0.3,
            max_tokens=1000
        )

        choice = response.choices[0].message
        
        result = {
            "text": choice.content,
            "tool_calls": []
        }

        if choice.tool_calls:
            for tc in choice.tool_calls:
                result["tool_calls"].append({
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                })
                
        return result
