import os
import json

class ConfigurationManager:
    """Central configuration engine managing user preferences securely."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_default_config()
        self._load()

    def _load_default_config(self) -> dict:
        return {
            "identity": {
                "jarvis_name": "JARVIS",
                "user_name": "User",
            },
            "activation": {
                "wake_word": "jarvis",
                "hotkey": "ctrl+space"
            },
            "ai_providers": {
                "default": "groq",
                "models": {
                    "groq": "openai/gpt-oss-20b"
                }
            },
            "features": {
                "voice_input": True,
                "voice_output": True,
                "screen_capture": True,
                "gmail": True,
                "calendar": True,
                "coding_agent": True
            }
        }

    def _load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    # Simple merge
                    self._deep_update(self.config, user_config)
            except Exception as e:
                print(f"[ConfigManager] Error loading config: {e}. Using defaults.")
        else:
            self._save()

    def _save(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"[ConfigManager] Error saving config: {e}")

    def _deep_update(self, d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = self._deep_update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def get(self, path: str, default=None):
        """Get config by dotted path (e.g. 'identity.jarvis_name')"""
        keys = path.split(".")
        val = self.config
        try:
            for key in keys:
                val = val[key]
            return val
        except KeyError:
            return default

    def set(self, path: str, value):
        """Set config by dotted path and save."""
        keys = path.split(".")
        d = self.config
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value
        self._save()

config_manager = ConfigurationManager()
