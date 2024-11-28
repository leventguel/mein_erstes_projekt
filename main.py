from cli_interface import run_cli
# Placeholder for GUI import if needed later
from gui_interface import run_gui

def main():
    print("Welcome to the Poem Management System!")
    print("1. Command-Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    
    while True:
        choice = input("Choose an interface (1 for CLI, 2 for GUI, or 'q' to quit): ").strip()
        if choice == '1':
            run_cli()
        elif choice == '2':
            #print("GUI is not implemented yet.")
            run_gui()  # This will execute the GUI setup from gui_interface.py
        elif choice.lower() == 'q':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
