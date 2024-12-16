import os
import sys
import time
import threading
import tkinter as tk
from event_manager import EventManager, FileImportEventManager
from gui_interface import run_gui, reset_cli_prompt, PoemApp, GUIObserver
from cli_interface import run_cli
from helpers import recreate_table_preserve_order
from poem_operations import show_all_poems, add_poem

def flush_input():
    """Flush the input buffer."""
    try:
        import msvcrt  # Windows
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import termios  # Linux/Unix
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

def cli_menu(event_manager):
    """CLI-Menu in einem separaten Thread ausführen."""
    while True:
        print("Welcome to the Poem Management System!")
        print("1. Command-Line Interface (CLI)")
        print("2. Graphical User Interface (GUI)")
        choice = input("Choose an option (1-2, or 'q' to quit): ").strip()

        if choice == '1':
            print("Running CLI...")
            # Hier CLI-Funktionen aufrufen
        elif choice == '2':
            print("Switching to GUI...")
            event_manager.notify("switch_to_gui")
        elif choice.lower() == 'q':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
def show_poems_in_gui(event_manager):
    """Show poems in the GUI."""
    # We don't need to create the root window here, it's done in `run_gui` inside the GUI code
    #run_gui(event_manager)  # Run GUI with the event_manager passed as a parameter
    """Run GUI in a separate thread."""
    run_gui(event_manager)
    print("GUI geschlossen. Zurück zum CLI.")  # Zurück zum CLI

def show_poems_in_gui(event_manager, observer):
    """Show poems in the GUI."""
    root = tk.Tk()
    app = PoemApp(root, event_manager, observer)
    app.run()
    print("Returned to CLI after GUI closed.")

def display_poems_in_cli(event_manager):
    """Display poems in the CLI and return to the menu."""
    run_cli(event_manager)  # Display poems in the CLI

def main():
    # Initialize the event manager
    event_manager = EventManager()

    # Create the GUI observer instance
    observer = GUIObserver()

    global app
    if PoemApp._instance is not None:  # Reset the singleton instance
        PoemApp._instance = None

        
    while True:
        # Print the menu options
        print("Welcome to the Poem Management System!")
        print("1. Command-Line Interface (CLI)")
        print("2. Graphical User Interface (GUI)")
        
        flush_input()
        choice = input("Choose an option (1-2, or 'q' to quit): ").strip()

        if choice == '1':
            #run_cli(event_manager)  # Pass the event manager to CLI
            display_poems_in_cli(event_manager)  # Show poems in the CLI and return to the menu
        elif choice == '2':
            #run_gui(event_manager)  # Launch the GUI asynchronously
            show_poems_in_gui(event_manager, observer)  # Show poems in the GUI

        elif choice.lower() == 'q':
            print("Exiting. Goodbye!")
            break  # Exit the loop and end the program
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
