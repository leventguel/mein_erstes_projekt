import os
import glob
from helpers import recreate_table_preserve_order
from poem_operations import add_poem, show_all_poems, delete_poem, import_poem_from_file
from translations import MENU_TRANSLATIONS
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion, WordCompleter  # Ensure these are imported correctly
from event_manager import FileImportEventManager

# Create a global event manager instance
event_manager = FileImportEventManager()

# CLIObserver class definition
class CLIObserver:
    def update(self, event, data):
        if event == "file_import_status_changed":
            if data['active']:
                print(f"CLI: File import is active. File path: {data['file_path']}")
            else:
                print("CLI: File import has been completed or canceled.")

# Path Completer for file path auto-completion using glob
class PathCompleter(Completer):
    def __init__(self, only_directories=True):
        self.only_directories = only_directories

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if os.path.isdir(text):  # If it's a directory, complete the directories
            matches = glob.glob(os.path.join(text, '*'))
        elif not self.only_directories:  # If it's not restricted to directories, allow files
            matches = glob.glob(os.path.join(text, '*'))
        else:
            matches = []

        for match in matches:
            yield Completion(match, start_position=-len(text))

# Command Completer for the actions in your CLI menu
class CommandCompleter(WordCompleter):
    def __init__(self, commands):
        super().__init__(commands, ignore_case=True)

# Main CLI function
def run_cli(event_manager):
    language = "en"  # Default session language
    translations = MENU_TRANSLATIONS[language]

    # Register the observer for event handling
    cli_observer = CLIObserver()  # Initialize the observer
    event_manager.register_observer(cli_observer)  # Register the observer to the event manager

    # CLI commands mapping
    cli_commands = {
        '1': translations['add_poem'],
        '2': translations['show_all'],
        '3': translations['delete_poem'],
        '4': translations['change_language'],
        '5': translations['file_import'],
        '6': translations['exit'],
    }

    while True:
        # Display the menu with Exit as the last option
        print("\n" + translations['menu_title'])
        for key, command in cli_commands.items():
            print(f"{key}. {command}")

        # Prompt the user for their action
        choice = prompt(translations['choose_action'], completer=CommandCompleter(list(cli_commands.keys()))).strip()

        # Handle the user choice based on input
        if choice == '1':
            title = prompt(f"{translations['add_poem']}: ")
            content = prompt("Enter poem content: ")
            add_poem(language, title, content)

        elif choice == '2':
            show_all_poems(language, output_to_cli=True, return_as_dict=False)  # Print poems to CLI

        elif choice == '3':
            poem_id = prompt("Enter poem ID to delete: ").strip()
            if poem_id.isdigit():
                delete_poem(language, int(poem_id))
            else:
                print("Invalid ID. Please try again.")

        elif choice == '4':
            print("Available languages:", ", ".join(MENU_TRANSLATIONS.keys()))
            new_language = prompt("Enter the language code (e.g., 'en', 'de', 'fr'): ").strip()
            if new_language in MENU_TRANSLATIONS:
                language = new_language
                translations = MENU_TRANSLATIONS[language]
                print(f"Language switched to {language}.")
            else:
                print("Invalid language code. Language remains unchanged.")

        elif choice == '5':  # Import poem from file option
            if event_manager.is_import_active():
                print("A file import operation is already in progress, please try later.")
            else:
                event_manager.start_import()
                import_poem_from_file(language)  # Call the existing file import function
                event_manager.finish_import()  # Mark the import as finished
                print("Poem imported successfully!")

        elif choice == '6':  # Exit option
            print(translations['exit'])
            break  # Exit the loop and the program

        else:
            print("Invalid choice. Please try again.")
