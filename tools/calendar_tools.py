from .base_tool import BaseTool
from security.security_manager import SecurityManager
from integrations.google_calendar.calendar_service import calendar_service

class ReadCalendarTool(BaseTool):
    @property
    def name(self) -> str:
        return "read_calendar"

    @property
    def description(self) -> str:
        return "Reads upcoming events from the user's Google Calendar."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer", 
                    "description": "Number of events to read (default 5)"
                }
            }
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_SAFE

    def execute(self, max_results: int = 5, **kwargs) -> str:
        return calendar_service.get_upcoming_events(max_results=max_results)

class CreateCalendarEventTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_calendar_event"

    @property
    def description(self) -> str:
        return "Schedules a new event on the user's Google Calendar. Start time must be in ISO format."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Title of the event"},
                "start_time": {"type": "string", "description": "ISO format start time, e.g. '2026-09-12T10:00:00'"},
                "end_time": {"type": "string", "description": "Optional ISO format end time"}
            },
            "required": ["summary", "start_time"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_SENSITIVE  # Level 2

    def execute(self, summary: str, start_time: str, end_time: str = None, **kwargs) -> str:
        return calendar_service.schedule_event(summary=summary, start_time=start_time, end_time=end_time)
