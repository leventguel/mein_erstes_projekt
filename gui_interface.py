import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
from translations import MENU_TRANSLATIONS
from helpers import recreate_table_preserve_order
from poem_operations import add_poem, show_all_poems, delete_poem, import_poem_from_file
from event_manager import FileImportEventManager

class GUIObserver:
    def update(self, event, data):
        """Handle events from the event manager and update the GUI accordingly."""
        if event == "file_import_status_changed":
            if data['active']:
                print(f"GUI: File import is active. File path: {data['file_path']}")
            else:
                print("GUI: File import has been completed or canceled.")

class PoemApp:
    def __init__(self, root, event_manager, observer):
        self.root = root
        self.language = "en"  # Default language
        self.translations = MENU_TRANSLATIONS[self.language]
        self.event_manager = event_manager  # Store event manager instance
        self.observer = observer  # Store observer

        # Set default font and size
        self.current_font = "Arial"  # Font name
        self.current_size = 12  # Font size
        
        self.root.title(self.translations['menu_title'])
        self.create_widgets()

        # Register observer to event manager
        self.event_manager.register_observer(self.observer)
        
        # Allow resizing the window
        self.root.resizable(True, True)


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

    def show_all_poems_gui(self):
        try:
            poems = show_all_poems(self.language, output_to_cli=True, return_as_dict=True)
            
            if poems:
                # Create Toplevel window for showing poems
                show_window = tk.Toplevel(self.root)
                show_window.title(self.translations['show_all'])
                
                # Make the window resizable and set a minimum size
                show_window.geometry("600x400")
                show_window.minsize(400, 300)
                
                # Frame to contain canvas and scrollbar
                scroll_frame = tk.Frame(show_window)
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
                    tk.Label(scrollable_frame, text=f"ID: {poem['id']}, Title: {poem['title']}", font=(self.current_font, self.current_size, "bold")).pack(anchor="w", pady=5)
                    tk.Label(scrollable_frame, text=poem['content'], wraplength=container_width-30, justify="left", font=(self.current_font, self.current_size)).pack(anchor="w", pady=5)
                    tk.Label(scrollable_frame, text="-" * 50).pack(anchor="w", pady=5)
                    
                # Bind mouse wheel scrolling to the canvas
                def on_mouse_wheel(event):
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                        
                # Bind the mouse wheel event to scroll the canvas
                show_window.bind_all("<MouseWheel>", on_mouse_wheel)
                        
            else:
                show_window = tk.Toplevel(self.root)
                show_window.title(self.translations['show_all'])
                tk.Label(show_window, text="No poems available.").pack(pady=20)

        except Exception as e:
            print(f"Error in show_all_poems_gui: {e}")
            messagebox.showerror(self.translations['menu_title'], "An error occurred while fetching poems.")


    def quit_application(self):
        """Method to handle quitting the application."""
        self.root.quit()
        self.root.destroy()  # Optional: This ensures the window is properly destroyed after quitting.
                
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
        content_entry = tk.Text(add_window, height=5, width=30)
        content_entry.pack(pady=5)

        def save_poem():
            title = title_entry.get()
            content = content_entry.get("1.0", tk.END).strip()
            if title and content:
                add_poem(self.language, title, content)
                messagebox.showinfo(self.translations['menu_title'], "Poem added successfully!")
                add_window.destroy()
            else:
                messagebox.showerror(self.translations['menu_title'], "Please fill in all fields.")

        tk.Button(add_window, text="Save", command=save_poem).pack(pady=5)

    def delete_poem(self):
        """Delete a poem (this is just a placeholder for now)."""
        messagebox.showinfo(self.translations['menu_title'], "Delete Poem functionality is not implemented yet.")

    def import_poem_from_file_gui(self):
        """Handle the importing of a poem from a file."""
        if self.event_manager.is_import_active():
            print("File import is already in progress.")
            return

        file_path = filedialog.askopenfilename(title="Select a poem file")
        if file_path:
            self.event_manager.set_file_import_status(True, file_path)
            # Simulate adding the poem to the system
            with open(file_path, 'r', encoding='utf-8') as file:
                # title = file.name.split("/")[-1]  # Use filename as title
                title = os.path.splitext(os.path.basename(file_path))[0]  # Use filename without extension as title
                content = file.read()
                add_poem(self.language, title, content)
            self.event_manager.set_file_import_status(False, None)  # Reset import status after the process is complete

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

def run_gui(event_manager):
    observer = GUIObserver()  # Create the observer instance
    root = tk.Tk()
    app = PoemApp(root, event_manager, observer)  # Pass event_manager and observer to the PoemApp class
    root.mainloop()
