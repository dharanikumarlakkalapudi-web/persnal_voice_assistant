import os
import pickle
import base64
import glob
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from integrations.integration_manager import integration_manager

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]

class GmailService:
    def __init__(self):
        # We assume the user has placed credentials.json in e:\jarvis
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
                    integration_manager.set_status("gmail", "error", "credentials.json not found")
                    return None
                
                # If we're strictly a background service now, popping up a browser might hang.
                # For Phase 4 we will allow it to pop up a browser if run manually, 
                # but log it properly.
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    integration_manager.set_status("gmail", "error", f"Auth failed: {str(e)}")
                    return None
                
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        integration_manager.set_status("gmail", "connected")
        return build('gmail', 'v1', credentials=creds)

    def clean_text(self, text):
        if not text: return ""
        try:
            soup = BeautifulSoup(text, "html.parser")
            return soup.get_text(separator=' ', strip=True)
        except:
            return text.strip()

    def read_unread_emails(self, max_results=3, account_name=None):
        if account_name and account_name.lower() != "all":
            target_file = f"token_{account_name.lower()}.json"
            if os.path.exists(os.path.join(self.base_dir, target_file)):
                token_files = [target_file]
            elif account_name.lower() == "default" and os.path.exists(os.path.join(self.base_dir, "token.json")):
                token_files = ["token.json"]
            else:
                return f"Could not find an email account linked as '{account_name}'."
        else:
            token_files = [os.path.basename(f) for f in glob.glob(os.path.join(self.base_dir, 'token*.json'))]
            if not token_files:
                token_files = ['token.json']

        all_email_summaries = []
        
        for token_file in token_files:
            service = self.get_service(token_file)
            if not service:
                all_email_summaries.append(f"Failed to access Gmail for {token_file}.")
                continue

            try:
                profile = service.users().getProfile(userId='me').execute()
                email_address = profile.get('emailAddress', f'Unknown Account ({token_file})')
                
                results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=max_results).execute()
                messages = results.get('messages', [])

                if not messages:
                    all_email_summaries.append(f"Inbox: {email_address} - You have no unread emails!")
                    continue

                email_summaries = []
                for index, message in enumerate(messages):
                    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                    payload = msg['payload']
                    headers = payload.get("headers")
                    parts = payload.get("parts")
                    
                    subject = "No Subject"
                    sender = "Unknown Sender"
                    
                    if headers:
                        for d in headers:
                            if d['name'] == 'Subject': subject = d['value']
                            if d['name'] == 'From': sender = d['value']
                    
                    body = ""
                    if 'data' in payload.get('body', {}):
                        data = payload['body']['data']
                        body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    elif parts:
                        for part in parts:
                            if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                                data = part['body']['data']
                                body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    
                    body = self.clean_text(body)[:3000]
                    email_summaries.append(f"Email {index+1}:\nFrom: {sender}\nSubject: {subject}\nSnippet: {body}\n")

                account_summary = f"Inbox: {email_address}\n" + "\n".join(email_summaries)
                all_email_summaries.append(account_summary)

            except Exception as error:
                all_email_summaries.append(f"An error occurred while fetching emails for {token_file}: {error}")

        return "\n\n".join(all_email_summaries)

gmail_service = GmailService()
