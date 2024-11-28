# event_manager.py
class EventManager:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        """Register an observer."""
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer):
        """Unregister an observer."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event, data=None):
        """Notify all observers about an event."""
        for observer in self._observers:
            observer.update(event, data)

class FileImportEventManager:
    def __init__(self):
        self.observers = []  # List to hold observers
        self.file_import_active = False
        self.file_path = None

    def register_observer(self, observer):
        """Registers an observer to be notified of events."""
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        """Removes an observer."""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, event, data):
        """Notifies all registered observers of an event."""
        for observer in self.observers:
            observer.update(event, data)

    def set_file_import_status(self, active, file_path=None):
        """Sets the status of the file import operation and notifies observers."""
        self.file_import_active = active
        self.file_path = file_path
        self.notify_observers("file_import_status_changed", {
            "active": self.file_import_active,
            "file_path": self.file_path
        })

    def is_import_active(self):
        """Returns the current status of the file import operation."""
        return self.file_import_active

    def start_import(self):
        """Start a new file import."""
        self.set_file_import_status(True)

    def finish_import(self):
        """Finish the current file import."""
        self.set_file_import_status(False)
