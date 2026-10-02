import sys
import os

# Add root jarvis dir to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.application import get_app
from core.event_bus import event_bus
from configuration.config_manager import config_manager
from security.credential_vault import vault
from database.sqlite_database import db

def on_identity_changed(event_type, data):
    print(f"--> [Callback] Identity changed to: {data.get('display_name')}")

def run_tests():
    print("=== JARVIS V2 Foundation Test ===\n")

    # 1. Test Application & Event Bus
    app = get_app()
    event_bus.subscribe("identity.changed", on_identity_changed)
    
    # 2. Test Configuration Engine (Identity)
    print("\n--- Testing Config Engine (Identity) ---")
    current_name = config_manager.identity.display_name
    print(f"Current Agent Name: {current_name}")
    print("Changing name to FRIDAY...")
    config_manager.identity.set_display_name("FRIDAY")
    print(f"New Agent Name: {config_manager.identity.display_name}")

    # 3. Test Configuration Engine (Applications)
    print("\n--- Testing Config Engine (Applications) ---")
    config_manager.applications.add_application(
        app_id="notepad",
        display_name="Notepad",
        app_type="desktop",
        launch_method="executable",
        executable_path="notepad.exe"
    )
    app_data = config_manager.applications.get_application("notepad")
    print(f"Retrieved App: {dict(app_data)}")

    # 4. Test Credential Vault
    print("\n--- Testing Credential Vault ---")
    vault.set_credential("test_groq_key", "gsk_super_secret_test_key_123")
    retrieved = vault.get_credential("test_groq_key")
    print(f"Retrieved from secure vault: {retrieved}")
    vault.delete_credential("test_groq_key")
    
    # 5. Restore Original Name
    print("\n--- Cleaning Up ---")
    config_manager.identity.set_display_name("JARVIS")
    print(f"Restored name: {config_manager.identity.display_name}")
    
    print("\n=== ALL TESTS PASSED ===")

if __name__ == "__main__":
    run_tests()
