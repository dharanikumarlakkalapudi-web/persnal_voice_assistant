class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: str, callback: callable):
        """Subscribe a callback to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: callable):
        """Remove a callback from an event type."""
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(callback)
            except ValueError:
                pass

    def publish(self, event_type: str, data: dict = None):
        """Publish an event to all subscribers."""
        if data is None:
            data = {}
        
        print(f"[EventBus] Published: {event_type}")
        
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event_type, data)
                except Exception as e:
                    print(f"[EventBus Error] Exception in subscriber for {event_type}: {e}")

# Global singleton
event_bus = EventBus()
