from database.sqlite_database import db
from core.event_bus import event_bus

class HotkeyManager:
    def set_hotkey(self, action_id, key_combination):
        db.execute(
            "INSERT OR REPLACE INTO hotkeys (action_id, key_combination, enabled) VALUES (?, ?, 1)",
            (action_id, key_combination)
        )
        event_bus.publish("hotkey.updated", {"action_id": action_id, "key_combination": key_combination})

    def get_hotkey(self, action_id):
        row = db.fetchone("SELECT key_combination FROM hotkeys WHERE action_id=? AND enabled=1", (action_id,))
        return row["key_combination"] if row else None
