# event_manager.py
from threading import Event
class EventManager:
    _instance = None
    _observers = {}
    
    def __init__(self):
        self._observers = {}
        self._poems_displayed_event = Event()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def reset(self):
        """Reset the state of the event manager."""
        self._observers = {}  # Clear all observers when resetting

    def register(self, event, observer):
        """Register an observer for a specific event."""
        if event not in self._observers:
            self._observers[event] = []
            self._observers[event].append(observer)

    def unregister(self, event, observer):
        """Unregister an observer for a specific event type."""
        if event in self._observers and observer in self._observers[event]:
            self._observers[event].remove(observer)

    def signal_poems_displayed(self):
        print("Signaling CLI: Poems were displayed.")
        self._poems_displayed_event.set()
        
    def wait_for_poems_displayed(self):
        print("CLI is waiting for GUI to finish displaying poems...")
        self._poems_displayed_event.wait()  # Block until event is triggered
        self._poems_displayed_event.clear()  # Reset for future use

    def is_poems_displayed(self):
        return self._poems_displayed_event

    def notify(self, event, data):
        """Notify all registered observers of an event."""
        if event in self._observers:
            for observer in self._observers[event]:
                observer.update(event, data)

class FileImportEventManager:
    def __init__(self, event_manager):
        """Specialized event manager for file imports."""
        self.event_manager = event_manager
        self.file_import_active = False
        self.file_path = None

    def register_observer(self, observer):
        """Register an observer for file import events."""
        self.event_manager.register("file_import_status_changed", observer)

    def remove_observer(self, observer):
        """Remove an observer for file import events."""
        self.event_manager.unregister("file_import_status_changed", observer)

    def set_file_import_status(self, active, file_path=None):
        """Set file import status and notify observers."""
        self.file_import_active = active
        self.file_path = file_path
        self.event_manager.notify("file_import_status_changed", {
            "active": self.file_import_active,
            "file_path": self.file_path
        })

    def is_import_active(self):
        """Check if file import is active."""
        return self.file_import_active

    def start_import(self):
        """Start file import."""
        self.set_file_import_status(True)

    def finish_import(self):
        """Finish file import."""
        self.set_file_import_status(False)

    def error_occurred(self, error_message):
        self.event_manager.notify("file_import_error", {"error": error_message})

class FileImportObserver:
    def update(self, event_type, data):
        if event_type == "file_import_status_changed":
            print(f"File import status changed: {data}")
