import os
from core.event_bus import event_bus

class IntegrationManager:
    def __init__(self):
        # For Phase 4, we maintain basic in-memory status. 
        # In the future, this would sync with an `integration_accounts` SQLite table.
        self._status = {}

    def set_status(self, integration_id: str, status: str, message: str = ""):
        self._status[integration_id] = {"status": status, "message": message}
        event_bus.publish("integration.status_changed", {"id": integration_id, "status": status})

    def get_status(self, integration_id: str):
        return self._status.get(integration_id, {"status": "unknown", "message": ""})

integration_manager = IntegrationManager()
