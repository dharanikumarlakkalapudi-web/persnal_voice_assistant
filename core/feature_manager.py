from configuration.manager import config_manager

class FeatureManager:
    """Central registry that checks if features are enabled."""
    
    def __init__(self):
        # Maps feature IDs to their dotted config paths
        self.feature_map = {
            "voice_input": "features.voice_input",
            "voice_output": "features.voice_output",
            "screen_capture": "features.screen_capture",
            "gmail": "features.gmail",
            "calendar": "features.calendar",
            "coding_agent": "features.coding_agent",
            "terminal": "features.terminal",
        }

    def is_feature_enabled(self, feature_id: str) -> bool:
        if feature_id not in self.feature_map:
            # If a feature isn't explicitly tracked, assume True for now,
            # or could default to False for strict security.
            return True
            
        config_path = self.feature_map[feature_id]
        return config_manager.get(config_path, default=False)

feature_manager = FeatureManager()
