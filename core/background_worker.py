import threading
import time
from core.event_bus import event_bus
from core.agent_orchestrator import AgentOrchestrator

class BackgroundWorker:
    def __init__(self, interval_seconds: int = 300):
        self.interval = interval_seconds
        self.running = False
        self.thread = None
        self.orchestrator = AgentOrchestrator(verbose=False)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        event_bus.publish("background_worker.started", {"interval": self.interval})
        print(f"[BackgroundWorker] Started with interval {self.interval}s.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        event_bus.publish("background_worker.stopped", {})
        print("[BackgroundWorker] Stopped.")

    def _loop(self):
        import json
        import os
        while self.running:
            print("\n[BackgroundWorker] Waking up for routine check...")
            try:
                automations = []
                if os.path.exists("automations.json"):
                    with open("automations.json", "r") as f:
                        automations = json.load(f)
                else:
                    # Fallback default
                    automations = [{
                        "id": "urgent_email_check",
                        "prompt": "Check unread emails. If there is anything highly urgent, summarize it as an alert. Otherwise, respond exactly with 'NO_ALERT'."
                    }]
                    
                for auto in automations:
                    print(f"[BackgroundWorker] Running automation: {auto.get('id', 'unknown')}")
                    query = f"[HINT: Route to proactive_agent] {auto['prompt']}"
                    
                    response = self.orchestrator.process_request(query)
                    
                    if "NO_ALERT" not in response and response.strip() != "":
                        print("\n!!! [URGENT PROACTIVE ALERT] !!!")
                        print(response)
                        event_bus.publish("proactive.alert", {"message": response, "id": auto.get('id')})
                    else:
                        print(f"[BackgroundWorker] {auto.get('id')} finished. Nothing urgent.")
                        
            except Exception as e:
                print(f"[BackgroundWorker] Error during check: {e}")
                
            for _ in range(int(self.interval)):
                if not self.running:
                    break
                time.sleep(1)

background_worker = BackgroundWorker()
