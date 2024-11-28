from cli_interface import run_cli
from gui_interface import run_gui
from event_manager import FileImportEventManager  # Import EventManager

def main():
    print("Welcome to the Poem Management System!")
    print("1. Command-Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")

    # Create an instance of the event manager
    event_manager = FileImportEventManager()

    while True:
        choice = input("Choose an interface (1 for CLI, 2 for GUI, or 'q' to quit): ").strip()
        if choice == '1':
            run_cli(event_manager)  # Pass the event manager to CLI
        elif choice == '2':
            run_gui(event_manager)  # Pass the event manager to GUI
        elif choice.lower() == 'q':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
