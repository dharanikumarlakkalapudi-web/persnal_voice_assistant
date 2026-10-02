import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from integrations.integration_manager import integration_manager

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]

class CalendarService:
    def __init__(self):
        self.creds_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "credentials.json")
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    def get_service(self, token_file='token.json'):
        creds = None
        token_path = os.path.join(self.base_dir, token_file)
        
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    if os.path.exists(token_path):
                        os.remove(token_path)
                    creds = None
                    
            if not creds:
                if not os.path.exists(self.creds_path):
                    integration_manager.set_status("google_calendar", "error", "credentials.json not found")
                    return None
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    integration_manager.set_status("google_calendar", "error", f"Auth failed: {str(e)}")
                    return None
                    
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        integration_manager.set_status("google_calendar", "connected")
        return build('calendar', 'v3', credentials=creds)

    def get_upcoming_events(self, max_results=5) -> str:
        service = self.get_service()
        if not service:
            return "Failed to authenticate Calendar API."

        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(
                calendarId='primary', timeMin=now,
                maxResults=max_results, singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])

            if not events:
                return "You have no upcoming calendar events."

            output = ["Upcoming Calendar Events:"]
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                try:
                    dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                    start_str = dt.strftime("%B %d at %I:%M %p")
                except:
                    start_str = start
                output.append(f"- {event['summary']} (Starts: {start_str})")
                
            return "\n".join(output)
        except Exception as e:
            return f"Failed to fetch calendar events: {e}"

    def schedule_event(self, summary: str, start_time: str, end_time: str = None) -> str:
        service = self.get_service()
        if not service:
            return "Failed to authenticate Calendar API."
            
        try:
            if not end_time:
                start_dt = datetime.datetime.fromisoformat(start_time)
                end_dt = start_dt + datetime.timedelta(hours=1)
                end_time = end_dt.isoformat()
                
            event = {
              'summary': summary,
              'start': {
                'dateTime': start_time + '+05:30',
                'timeZone': 'Asia/Kolkata',
              },
              'end': {
                'dateTime': end_time + '+05:30',
                'timeZone': 'Asia/Kolkata',
              },
            }

            event_result = service.events().insert(calendarId='primary', body=event).execute()
            return f"Event created successfully: {event_result.get('htmlLink')}"
        except Exception as e:
            return f"Failed to schedule event: {e}"

calendar_service = CalendarService()
