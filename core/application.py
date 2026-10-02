from core.event_bus import event_bus
from database.sqlite_database import db

class JarvisApplication:
    """The central application bootstrap class."""
    def __init__(self):
        self.state = "INITIALIZING"
        self._bootstrap()

    def _bootstrap(self):
        print("[Application] Bootstrapping JARVIS V2...")
        # In a real setup we would instantiate managers here.
        # e.g. self.config_manager = ConfigManager()
        # self.security_manager = SecurityManager()
        
        self.state = "READY"
        event_bus.publish("application.ready")

    def shutdown(self):
        print("[Application] Shutting down...")
        self.state = "SHUTTING_DOWN"
        event_bus.publish("application.shutdown")

# Global app instance
app_instance = None

def get_app():
    global app_instance
    if app_instance is None:
        app_instance = JarvisApplication()
    return app_instance
