import sys
import os

# Add the root directory to path so we can import from integrations
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from integrations.gmail.gmail_service import gmail_service

def main():
    print("=== Jarvis Email Authenticator ===")
    print("Enter a name for this account (e.g., 'college', 'personal', 'work').")
    print("If you enter 'personal', it will create 'token_personal.json'.")
    
    account_name = input("\nAccount Name: ").strip().lower()
    if not account_name:
        print("Invalid account name.")
        return
        
    token_filename = f"token_{account_name}.json"
    print(f"\nAttempting to authenticate and generate {token_filename}...")
    
    try:
        # This will trigger the web browser OAuth flow if the token doesn't exist
        service = gmail_service.get_service(token_filename)
        
        if service:
            print(f"\n✅ Success! Authenticated successfully.")
            print(f"You can now tell Jarvis to 'read my {account_name} emails'.")
        else:
            print(f"\n❌ Failed to authenticate. Ensure credentials.json is valid.")
            
    except Exception as e:
        print(f"\n❌ Error during authentication: {e}")

if __name__ == "__main__":
    main()
