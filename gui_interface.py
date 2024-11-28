import tkinter as tk
from tkinter import messagebox
from translations import MENU_TRANSLATIONS
from poem_operations import add_poem, show_all_poems, delete_poem

class PoemApp:
    def __init__(self, root):
        self.root = root
        self.language = "en"  # Default language
        self.translations = MENU_TRANSLATIONS[self.language]

        self.root.title(self.translations['menu_title'])
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
    
        self.language_button = tk.Button(self.root, text=self.translations['change_language'], command=self.change_language)
        self.language_button.pack(pady=5)
        
        # Quit button now explicitly calls root.quit() to ensure the window can be closed
        self.exit_button = tk.Button(self.root, text=self.translations['exit'], command=self.quit_application)
        self.exit_button.pack(pady=5)
        
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

    def show_all_poems_gui(self):
        try:
            poems = show_all_poems(self.language)
            show_window = tk.Toplevel(self.root)
            show_window.title(self.translations['show_all'])
            
            # Add a scrollable frame or text area to display poems
            if poems:
                scroll_frame = tk.Frame(show_window)
                scroll_frame.pack(padx=10, pady=10)
                
                canvas = tk.Canvas(scroll_frame)
                scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
                canvas.configure(yscrollcommand=scrollbar.set)
                
                scrollable_frame = tk.Frame(canvas)
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.grid(row=0, column=0, sticky="nsew")
                scrollbar.grid(row=0, column=1, sticky="ns")
                
                for poem in poems:
                    tk.Label(scrollable_frame, text=f"ID: {poem['id']}, Title: {poem['title']}", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
                    tk.Label(scrollable_frame, text=poem['content'], wraplength=300, justify="left").pack(anchor="w", pady=5)
                    tk.Label(scrollable_frame, text="-" * 50).pack(anchor="w", pady=5)
                else:
                    tk.Label(show_window, text="No poems available.").pack(pady=20)
        except Exception as e:
            print(f"Error in show_all_poems_gui: {e}")
            messagebox.showerror(self.translations['menu_title'], "An error occurred while fetching poems.")


    def delete_poem(self):
        """Delete a poem by ID via a popup dialog."""
        delete_window = tk.Toplevel(self.root)
        delete_window.title(self.translations['delete_poem'])

        tk.Label(delete_window, text="Enter Poem ID to delete:").pack(pady=5)
        id_entry = tk.Entry(delete_window)
        id_entry.pack(pady=5)

        def confirm_delete():
            poem_id = id_entry.get().strip()
            if poem_id.isdigit():
                delete_poem(self.language, int(poem_id))
                messagebox.showinfo(self.translations['menu_title'], "Poem deleted successfully!")
                delete_window.destroy()
            else:
                messagebox.showerror(self.translations['menu_title'], "Invalid ID. Please try again.")

        tk.Button(delete_window, text="Delete", command=confirm_delete).pack(pady=5)

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

def run_gui():
    root = tk.Tk()
    app = PoemApp(root)
    root.mainloop()
