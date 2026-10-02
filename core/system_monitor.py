import psutil
import time
import threading
from core.event_bus import event_bus

class SystemMonitor(threading.Thread):
    def __init__(self, interval=3.0):
        super().__init__(daemon=True)
        self.interval = interval
        self.running = False

    def run(self):
        self.running = True
        print("[SystemMonitor] Started collecting metrics.")
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=None)
                # Memory in GB
                mem = psutil.virtual_memory()
                ram_gb = round(mem.used / (1024 ** 3), 1)

                event_bus.publish("system.metrics", {
                    "cpu": cpu,
                    "ram": ram_gb,
                    "mic": True,      # Assume mic is connected
                    "camera": True,   # Assume camera is connected
                    "security": True
                })
            except Exception as e:
                print(f"[SystemMonitor Error] {e}")
            
            time.sleep(self.interval)

    def stop(self):
        self.running = False

system_monitor = SystemMonitor()
