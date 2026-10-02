from database.sqlite_database import db
from core.event_bus import event_bus

class IdentityManager:
    def __init__(self):
        self.agent_id = "personal_agent"
        # Attempt to load from DB, or set defaults
        row = db.fetchone("SELECT * FROM agents WHERE agent_id=?", (self.agent_id,))
        if not row:
            db.execute(
                "INSERT INTO agents (agent_id, display_name, provider, model, permissions_profile) VALUES (?, ?, ?, ?, ?)",
                (self.agent_id, "JARVIS", "groq", "llama-3.1-8b-instant", "balanced")
            )
            row = db.fetchone("SELECT * FROM agents WHERE agent_id=?", (self.agent_id,))
            
        self._cache = dict(row) if row else {}

    @property
    def display_name(self):
        return self._cache.get("display_name", "JARVIS")

    def set_display_name(self, new_name):
        db.execute("UPDATE agents SET display_name=? WHERE agent_id=?", (new_name, self.agent_id))
        self._cache["display_name"] = new_name
        event_bus.publish("identity.changed", {"display_name": new_name})
