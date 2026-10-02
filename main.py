import os
import sys
import threading
import uvicorn

# Ensure proper paths
sys.path.append(os.path.dirname(__file__))

from core.application import get_app
from core.background_worker import background_worker
from core.voice_worker import voice_worker
from core.system_monitor import system_monitor
import tools

def start_fastapi():
    print("[FastAPI] Starting WebSocket server at http://127.0.0.1:8001")
    uvicorn.run("core.server:app", host="127.0.0.1", port=8001, log_level="error")

def main():
    print("========================================")
    print(" JARVIS V2 - OS INITIALIZATION          ")
    print("========================================")

    # 1. Boot core systems (Database, Vault, EventBus)
    print("[System] Bootstrapping core application...")
    get_app()

    from security.face_id import verify_user_face
    print("\n[Security] Initializing Face ID Verification...")
    if not verify_user_face():
        print("[Security] Face ID verification failed! Boot aborted.")
        sys.exit(1)
    print("[Security] Identity verified successfully.\n")

    # 2. Start the Background Threads
    print("[System] Starting background thread...")
    background_worker.start()
    
    print("[System] Starting voice listener thread...")
    # NOTE: Voice worker requires whisper model to load, takes ~15 seconds.
    voice_worker.start()

    print("[System] Starting system monitor thread...")
    system_monitor.start()

    # 3. Start the UI Server and Desktop Window
    try:
        api_thread = threading.Thread(target=start_fastapi, daemon=True)
        api_thread.start()
        
        import time
        import webview
        time.sleep(1) # give FastAPI time to bind the port
        
        print("[System] Starting Desktop Application Window...")
        webview.create_window('JARVIS', 'http://127.0.0.1:8001/', width=1280, height=800)
        webview.start(private_mode=True)
        
        # When window is closed, webview.start() returns.
        print("\n[System] Window closed. Shutting down JARVIS...")
        background_worker.stop()
        voice_worker.stop()
        system_monitor.stop()
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n[System] Shutting down...")
        background_worker.stop()
        voice_worker.stop()
        system_monitor.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
