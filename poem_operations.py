import os
import sys
import time
import glob
from datetime import datetime
from prompt_toolkit.completion import Completion
from langdetect import detect, LangDetectException
from helpers import insert_poem, fetch_all_poems, delete_poem_by_id
from prompt_toolkit import prompt


def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print("Error: File not found.")
        return False
    return True

def detect_language(content):
    """Detect the language of the content."""
    try:
        return detect(content)
    except LangDetectException:
        return "en"  # Default to English if detection fails

def add_poem(language, title, content):
    """Add a poem to the database."""
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_poem(language, title.strip(), content.strip(), date_added)
    print(f"Poem '{title}' added to {language} database successfully!")

def show_all_poems(language, output_to_cli=False, return_as_dict=True):
    """Show all poems stored in the database for the given language."""
    poems = fetch_all_poems(language)
    
    if not poems:
        print(f"No poems found for language: {language}")
        return []  # Return an empty list for GUI

    if output_to_cli:
        print_poems_cli(poems)

    if return_as_dict:
        return format_poems_for_gui(poems)
    else:
        return poems

def print_poems_cli(poems):
    """Helper function to print poems in a readable format for CLI."""
    for poem in poems:
        print(f"ID: {poem[0]}, Title: {poem[1]}, Date: {poem[3]}, Language: {poem[4]}")
        print("Content:")
        print(poem[2])  # Keeps the original line breaks
        print("-" * 40)

def format_poems_for_gui(poems):
    """Helper function to format poems into a dictionary for the GUI."""
    return [
        {
            'id': poem[0],
            'title': poem[1],
            'content': poem[2],
            'date_added': poem[3],
            'language': poem[4],
        }
        for poem in poems
    ]

def delete_poem(language, poem_id):
    """Delete a poem from the database."""
    affected_rows = delete_poem_by_id(language, poem_id)
    if affected_rows > 0:
        print(f"Poem with ID {poem_id} deleted successfully.")
    else:
        print(f"No poem found with ID {poem_id}.")

def import_poem_from_file(language):
    """Import a poem from a file."""
    try:
        file_completer = PathCompleter(only_directories=False)
        file_path = prompt("Please enter the file path: ", completer=file_completer)

        # Check if the path exists
        if not check_file_exists(file_path):
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='ISO-8859-1') as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                print("Error: Unable to read file due to encoding issues.")
                return

        # Strip empty lines before processing
        lines = [line.strip() for line in lines if line.strip()]
            
        # Assuming first line is the title, rest is content
        # Ensure file contains at least a title and content
        if len(lines) < 2 or not lines[0].strip() or not lines[1].strip():
            print("Error: File must contain at least a title and content.")
        return

        title = lines[0].strip()  # First line as title
        content = "".join(lines[1:]).strip()  # Rest as content

        # Add poem to database, including language
        add_poem(language, title, content)
        print(f"Poem '{title}' imported successfully from {file_path}.")

    except Exception as e:
        print(f"Error importing poem: {e}")

# Path Completer for file path auto-completion using glob
class PathCompleter:
    def __init__(self, only_directories=True):
        self.only_directories = only_directories

    def get_completions(self, document, complete_event):
        """Provide completions for file paths using tab completion."""
        text = document.text_before_cursor
        matches = []
        
        if os.path.isdir(text):  # If it's a directory, complete directories
            matches = glob.glob(os.path.join(text, '*'))
        elif not self.only_directories:  # If not restricted to directories, allow files
            matches = glob.glob(os.path.join(text, '*'))

        for match in matches:
            yield Completion(match, start_position=-len(text))
