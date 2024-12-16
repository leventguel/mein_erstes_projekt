import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
from translations import MENU_TRANSLATIONS
from helpers import recreate_table_preserve_order
from poem_operations import add_poem, show_all_poems, delete_poem, import_poem_from_file
from event_manager import FileImportEventManager

def reset_cli_prompt():
    """Helper function to reset CLI prompt format."""
    print("\nWelcome to the Poem Management System!")
    print("1. Command-Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")

class GUIObserver:
    def update(self, event, data):
        """Handle events from the event manager and update the GUI accordingly."""
        if event == "file_import_status_changed":
            if data['active']:
                print(f"GUI: File import is active. File path: {data['file_path']}")
            else:
                print("GUI: File import has been completed or canceled.")


class PoemApp:
    _instance = None  # Class variable to hold the singleton instance

    def __new__(cls, root, event_manager, observer):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, root, event_manager, observer):
        _instance = None
        if not hasattr(self, '_initialized'):  # Prevent reinitializing if already initialized
            self.root = root
            self.language = "en"  # Default language
            self.translations = MENU_TRANSLATIONS[self.language]
            self.poems_displayed = False  # Flag to track if poems have been displayed
            self.event_manager = event_manager  # Store event manager instance
            self.observer = observer  # Store observer

            # Set default font and size
            self.current_font = "Arial"  # Font name
            self.current_size = 12  # Font size

            self.title_label = tk.Label(self.root, text="Poem Management System")
            self.title_label.pack()

            self.root.title(self.translations['menu_title'])

            self.root.protocol("WM_DELETE_WINDOW", self.on_close)
            
            self.create_widgets()

            # Register observer to event manager
            self.event_manager.register("file_import_status_changed", self.observer)

            # Allow resizing the window
            self.root.resizable(True, True)

            self._initialized = True  # Prevent reinitializing
        else:
            # Recreate widgets if instance is reused
            self.create_widgets()


    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text=self.translations['menu_title'], font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Buttons for actions
        self.add_button = tk.Button(self.root, text=self.translations['add_poem'], command=self.add_poem)
        self.add_button.pack(pady=5)

        self.show_button = tk.Button(self.root, text=self.translations['show_all'], command=self.show_all_poems_gui)
        self.show_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text=self.translations['delete_poem'], command=self.delete_poem)
        self.delete_button.pack(pady=5)

        # New Import Poem from File Button
        self.import_button = tk.Button(self.root, text=self.translations['file_import'], command=self.import_poem_from_file_gui)
        self.import_button.pack(pady=5)

        self.language_button = tk.Button(self.root, text=self.translations['change_language'], command=self.change_language)
        self.language_button.pack(pady=5)

        # Font selection dropdown
        self.font_label = tk.Label(self.root, text="Font:")
        self.font_label.pack(pady=5)
        self.font_dropdown = ttk.Combobox(self.root, values=font.families())
        self.font_dropdown.set(self.current_font)  # Set default font
        self.font_dropdown.pack(pady=5)
        self.font_dropdown.bind("<<ComboboxSelected>>", self.update_font)

        # Size selection dropdown
        self.size_label = tk.Label(self.root, text="Size:")
        self.size_label.pack(pady=5)
        self.size_dropdown = ttk.Combobox(self.root, values=[8, 10, 12, 14, 16, 18, 20, 24, 28, 32])
        self.size_dropdown.set(self.current_size)  # Set default size
        self.size_dropdown.pack(pady=5)
        self.size_dropdown.bind("<<ComboboxSelected>>", self.update_size)

        # Quit button
        self.exit_button = tk.Button(self.root, text=self.translations['exit'], command=self.quit_application)
        self.exit_button.pack(pady=5)

    def update_font(self, event):
        """Update font of poem text based on user selection."""
        self.current_font = self.font_dropdown.get()  # Get the font name from the dropdown
        self.update_poem_text_widget()

    def update_size(self, event):
        """Update font size of poem text based on user selection."""
        self.current_size = int(self.size_dropdown.get())  # Get the font size from the dropdown
        self.update_poem_text_widget()

    def update_poem_text_widget(self):
        """Update the text widget's font and size."""
        if hasattr(self, 'poem_text_widget'):
            self.poem_text_widget.config(font=(self.current_font, self.current_size))

    def on_closing(self, event=None):
        
        """Handle the window closing event."""
        if self.poems_displayed:
            print("Poems were displayed, triggering event.")
            self.event_manager.signal_poems_displayed()  # Signal the event manager that we're done
            self.poems_displayed = False  # Reset the flag after displaying poems
        else:
            print("No poems were displayed.")
            
        # Check if the window exists and close it properly
        if self.show_window and self.show_window.winfo_exists():
            print("Closing poem window.")
            self.show_window.quit()  # Close the window
            self.show_window.destroy()  # Properly destroy the window
        else:
            print("Window already destroyed or non-existent.")
                
        print("Poem window closed.")
        #self.event_manager.signal_poems_displayed()  # Notify CLI that GUI is done
        self.show_window.destroy()

    def on_close(self):
        """Handle closing the window."""
        print("Window closed.")
        self.root.quit()  # Quit Tkinter's main loop
        self.root.destroy()  # Destroy the root window

    def run(self):
        """Start the GUI event loop."""
        self.root.mainloop()

    def show_all_poems_gui(self):
        try:
            # Fetch poems for both CLI and GUI
            poems = show_all_poems(self.language, output_to_cli=True, return_as_dict=True)
        
            if poems:
                # Create Toplevel window for showing poems
                if hasattr(self, 'show_window') and self.show_window.winfo_exists():
                    # Window already open, skip creation
                    print("Poem window is already open.")
                    return  # Exit early without creating a new window
                else:
                    # Create show_window as an attribute of the class instance
                    self.show_window = tk.Toplevel(self.root)
                    self.show_window.title(self.translations['show_all'])
                    
                    # Make the window resizable and set a minimum size
                    self.show_window.geometry("600x400")
                    self.show_window.minsize(400, 300)
                    
                    # Frame to contain canvas and scrollbar
                    scroll_frame = tk.Frame(self.show_window)
                    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)
                    
                    # Create a canvas inside the scroll_frame
                    canvas = tk.Canvas(scroll_frame)
                    canvas.pack(side="left", fill="both", expand=True)
                    
                    # Create a vertical scrollbar linked to the canvas
                    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
                    scrollbar.pack(side="right", fill="y")
                    
                    # Configure the canvas to work with the scrollbar
                    canvas.configure(yscrollcommand=scrollbar.set)
                    
                    # Create a frame inside the canvas to hold the poem content
                    scrollable_frame = tk.Frame(canvas)
                    
                    # Bind the scroll region to the size of the content
                    scrollable_frame.bind(
                        "<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                    )
                
                    # Create a window on the canvas to contain the scrollable_frame
                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                
                    # Add poems to the scrollable frame
                    for poem in poems:
                        # Use width of the container dynamically for wraplength
                        container_width = scroll_frame.winfo_width()
                    
                        # Create labels for title and content, adjust wraplength based on container width
                        tk.Label(scrollable_frame, text=poem['title'], font=(self.current_font, self.current_size, "bold")).pack(anchor="w", pady=5)
                        tk.Label(scrollable_frame, text=poem['content'], wraplength=container_width-30, justify="left", font=(self.current_font, self.current_size)).pack(anchor="w", pady=5)
                        tk.Label(scrollable_frame, text="-" * 50).pack(anchor="w", pady=5)
                    
                    # Bind mouse wheel scrolling to the canvas
                    def on_mouse_wheel(event):
                        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                    # Bind the mouse wheel event to scroll the canvas
                    self.show_window.bind_all("<MouseWheel>", on_mouse_wheel)
                
                    
                    # Notify CLI that the poems were displayed, no more input needed
                    #self.show_window.protocol("WM_DELETE_WINDOW", on_closing)
                    # Bind the close event only once to the on_closing function
                    self.show_window.protocol("WM_DELETE_WINDOW", self.on_closing)  # Register on_closing
                    self.poems_displayed = True  # Set flag when poems are displayed

                        
            else:
                self.show_window = tk.Toplevel(self.root)  # Create a window if poems not found
                self.show_window.title(self.translations['show_all'])
                tk.Label(self.show_window, text="No poems available.").pack(pady=20)
                    
        except Exception as e:
            print(f"Error in show_all_poems_gui: {e}")
            messagebox.showerror(self.translations['menu_title'], "An error occurred while fetching poems.")
        finally:
            reset_cli_prompt()

    '''
    def return_to_main_menu(self):
        if self.poems_displayed:
            self.poems_displayed = False  # Reset the flag
            self.event_manager.reset_poems_displayed_flag() # Reset the event flag
            print("Returning to main menu...")  # Do whatever is needed to return to the main menu
            # Your main menu logic here
            # Explicitly reset any other state variables, such as event signals
            #self.event_manager._poem_displayed_event_triggered = False
            #self.show_window = None  # Ensure the window object is reset if it was previously open
            #self.show_window.quit()
            #self.show_window.destroy()
            # Add a command to reset CLI state here, if necessary
        else:
            print("No poems were displayed. Returning to main menu without signaling.")
            # Additional logic to bring back the CLI menu if needed
    '''    
    def quit_application(self):
        """Method to handle quitting the application."""
        self.root.quit()
        self.root.destroy()  # Optional: This ensures the window is properly destroyed after quitting.

    def close_window(self):
        """Close the Tkinter window."""
        if self.root:
            self.root.destroy()  # Beendet das Hauptfenster korrekt
        print("Poem window closed.")

    def update_language(self):
        """Update all labels and buttons with the current language."""
        self.translations = MENU_TRANSLATIONS[self.language]
        self.root.title(self.translations['menu_title'])
        self.title_label.config(text=self.translations['menu_title'])
        self.add_button.config(text=self.translations['add_poem'])
        self.show_button.config(text=self.translations['show_all'])
        self.delete_button.config(text=self.translations['delete_poem'])
        self.import_button.config(text=self.translations['file_import'])  # Update new button text
        self.language_button.config(text=self.translations['change_language'])
        self.exit_button.config(text=self.translations['exit'])

    def add_poem(self):
        """Add a new poem via a popup dialog."""
        add_window = tk.Toplevel(self.root)
        add_window.title(self.translations['add_poem'])

        tk.Label(add_window, text="Title:").pack(pady=5)
        title_entry = tk.Entry(add_window)
        title_entry.pack(pady=5)

        tk.Label(add_window, text="Content:").pack(pady=5)
        content_entry = tk.Text(add_window, height=10, width=50)
        content_entry.pack(pady=5)

        def save_poem():
            title = title_entry.get()
            content = content_entry.get("1.0", "end-1c")
            add_poem(title, content, self.language)
            add_window.destroy()

        save_button = tk.Button(add_window, text="Save Poem", command=save_poem)
        save_button.pack(pady=5)

    def delete_poem(self):
        """Delete an existing poem via a dialog."""
        delete_window = tk.Toplevel(self.root)
        delete_window.title(self.translations['delete_poem'])

        tk.Label(delete_window, text="Enter Poem ID to delete:").pack(pady=5)
        id_entry = tk.Entry(delete_window)
        id_entry.pack(pady=5)

        def delete_selected_poem():
            poem_id = id_entry.get()
            delete_poem(poem_id, self.language)
            delete_window.destroy()

        delete_button = tk.Button(delete_window, text="Delete Poem", command=delete_selected_poem)
        delete_button.pack(pady=5)

    def import_poem_from_file_gui(self):
        """Handle poem import via file."""
        file_path = filedialog.askopenfilename(title="Select Poem File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            import_poem_from_file(file_path, self.language)
            messagebox.showinfo("File Import", f"Poem imported from {file_path}.")
        else:
            messagebox.showwarning("File Import", "No file selected.")

    def change_language(self):
        """Switch the application language."""
        lang_window = tk.Toplevel(self.root)
        lang_window.title(self.translations['change_language'])

        # Set a default size for the language selection window
        lang_window.geometry("300x200")

        tk.Label(lang_window, text="Available languages:").pack(pady=5)

        # Create buttons for each language option
        for lang_code in MENU_TRANSLATIONS.keys():
            tk.Button(lang_window, text=lang_code, command=lambda lc=lang_code: self.set_language(lc)).pack()

        # Ensure that the window is allowed to be moved and resized
        lang_window.resizable(True, True)  # Allow resizing in both directions (optional)
        lang_window.deiconify()  # Make sure the window is shown and not hidden

    def set_language(self, lang_code):
        """Set the current language."""
        self.language = lang_code
        self.update_language()
    

def run_gui(event_manager, root=False):
    """Run the GUI, passing the existing event manager."""
    
    # Create a new FileImportEventManager for the session
    file_import_event_manager = FileImportEventManager(event_manager)
    observer = GUIObserver()
    
    # Now, use the passed event_manager directly
    if not root:
        root = tk.Tk()
    
     # Bind the window close event to a custom function
    root.protocol("WM_DELETE_WINDOW", lambda: on_gui_close(root))
    
     # Create a new PoemApp instance
    app = PoemApp(root, event_manager, observer)  # Pass the existing event_manager

    # Start the Tkinter event loop
    root.mainloop()  # Start the GUI event loop
    #root.destroy()
