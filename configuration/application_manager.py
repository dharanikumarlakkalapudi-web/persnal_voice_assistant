from database.sqlite_database import db
from core.event_bus import event_bus

class ApplicationManager:
    def add_application(self, app_id, display_name, app_type, launch_method, executable_path=None, arguments=None, working_directory=None):
        db.execute(
            "INSERT OR REPLACE INTO applications (app_id, display_name, app_type, launch_method, executable_path, arguments, working_directory) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (app_id, display_name, app_type, launch_method, executable_path, arguments, working_directory)
        )
        event_bus.publish("application.updated", {"app_id": app_id})

    def get_application(self, app_id):
        return db.fetchone("SELECT * FROM applications WHERE app_id=?", (app_id,))

    def get_all_applications(self):
        return db.fetchall("SELECT * FROM applications WHERE enabled=1")
