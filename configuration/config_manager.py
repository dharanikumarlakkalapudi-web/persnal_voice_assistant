class ConfigManager:
    """Centralized configuration manager that other modules use."""
    def __init__(self):
        from .identity_manager import IdentityManager
        from .application_manager import ApplicationManager
        from .feature_manager import FeatureManager
        from .hotkey_manager import HotkeyManager

        self.identity = IdentityManager()
        self.applications = ApplicationManager()
        self.features = FeatureManager()
        self.hotkeys = HotkeyManager()

config_manager = ConfigManager()
