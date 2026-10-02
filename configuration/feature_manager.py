from database.sqlite_database import db
from core.event_bus import event_bus

class FeatureManager:
    def is_enabled(self, feature_id):
        row = db.fetchone("SELECT enabled FROM features WHERE feature_id=?", (feature_id,))
        return bool(row["enabled"]) if row else False

    def enable_feature(self, feature_id):
        db.execute("INSERT OR REPLACE INTO features (feature_id, enabled) VALUES (?, 1)", (feature_id,))
        event_bus.publish("feature.changed", {"feature_id": feature_id, "enabled": True})

    def disable_feature(self, feature_id):
        db.execute("UPDATE features SET enabled=0 WHERE feature_id=?", (feature_id,))
        event_bus.publish("feature.changed", {"feature_id": feature_id, "enabled": False})
