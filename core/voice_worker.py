import threading
import time
from datetime import datetime
from core.event_bus import event_bus
from core.agent_orchestrator import AgentOrchestrator
from voice import manager as voice

class VoiceWorker:
    def __init__(self):
        self.running = False
        self.thread = None
        self.orchestrator = AgentOrchestrator(verbose=True)
        self.is_sleeping = False

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        event_bus.publish("voice_worker.started", {})
        print("[VoiceWorker] Started continuous listening.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        event_bus.publish("voice_worker.stopped", {})
        print("[VoiceWorker] Stopped.")

    def _loop(self):
        # Give UI time to boot up
        time.sleep(3)
        event_bus.publish("voice.state", {"state": "SPEAKING"})
        msg = "I am back online with the new dashboard. How can I help?"
        event_bus.publish("voice.response", {"text": msg})
        voice.speak(msg)
        
        while self.running:
            try:
                if self.is_sleeping:
                    # Don't use microphone, just poll for hotkey to save CPU/privacy
                    time.sleep(0.1)
                    if voice.consume_hotkey():
                        self.is_sleeping = False
                        event_bus.publish("voice.state", {"state": "SPEAKING"})
                        voice.speak("I am awake. How can I help?")
                        event_bus.publish("voice.state", {"state": "IDLE"})
                    continue

                # 1. Listen for user input
                import winsound
                # Give a short beep before listening
                winsound.Beep(750, 150)
                
                event_bus.publish("voice.state", {"state": "LISTENING"})
                user_input = voice.listen()
                
                if not user_input or user_input.strip() == "":
                    event_bus.publish("voice.state", {"state": "IDLE"})
                    continue
                    
                print(f"[Voice Input]: {user_input}")
                
                # Check for multiple wake words
                from configuration.manager import config_manager
                wake_words = config_manager.get("activation.wake_words", ["jarvis"])
                hotkey_woke = voice.consume_hotkey()
                
                if not hotkey_woke and not any(ww.lower() in user_input.lower() for ww in wake_words):
                    print(f"(Debug: Ignoring input because no wake word ({', '.join(wake_words)}) or hotkey was found)")
                    event_bus.publish("voice.state", {"state": "IDLE"})
                    continue
                
                event_bus.publish("voice.transcript", {"text": user_input})
                
                if any(word in user_input.lower() for word in ['exit', 'quit']):
                    event_bus.publish("voice.state", {"state": "SPEAKING"})
                    voice.speak("Shutting down voice systems.")
                    self.stop()
                    break
                    
                if 'sleep' in user_input.lower() or 'stop listening' in user_input.lower():
                    self.is_sleeping = True
                    event_bus.publish("voice.state", {"state": "SPEAKING"})
                    voice.speak("Going to sleep. Press control space for waking up.")
                    event_bus.publish("voice.state", {"state": "IDLE"})
                    continue
                    
                print(f"Jarvis is thinking...")
                event_bus.publish("voice.state", {"state": "PROCESSING"})
                
                # 2. Process through Orchestrator
                response_text = self.orchestrator.process_request(user_input)
                
                # Publish the AI's response to the transcript
                event_bus.publish("voice.response", {"text": response_text})
                
                # 3. Speak the response
                event_bus.publish("voice.state", {"state": "SPEAKING"})
                voice.speak(response_text)
                event_bus.publish("voice.state", {"state": "IDLE"})
                
            except Exception as e:
                print(f"[VoiceWorker Error]: {str(e)}")
                event_bus.publish("voice.state", {"state": "ERROR"})
                time.sleep(2)

voice_worker = VoiceWorker()
