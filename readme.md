# Poem Management System

The **Poem Management System** is a Python-based application designed to create, manage, and display poems through both a **Graphical User Interface (GUI)** and a **Command-Line Interface (CLI)**. The system is built with modularity and extensibility in mind, making it a versatile tool for exploring text-based management systems.

> **Note**: This project is currently in development and is not yet feature-complete. Contributions and suggestions are welcome!

---

## Features

- **Add Poems**: Add new poems to the collection.
- **Show All Poems**: View the complete list of poems in the GUI or CLI.
- **Delete Poems**: (Feature placeholder - to be implemented).
- **File Import**: Import poems from external `.txt` files.
- **Multi-Language Support**: Easily switch between languages (currently limited to `en` and any others in `MENU_TRANSLATIONS`).
- **Custom Font and Size**: Customize the display font and size in the GUI.
- **Dynamic GUI**: The GUI adapts to different screen sizes and supports responsive resizing.

---

## Getting Started

### Prerequisites

- Python 3.8 or later
- Required libraries (install via pip):
  - `tkinter` (built-in with Python, includes `ttk` for advanced widgets)
  - `prompt_toolkit`
  - `sqlalchemy`
  - `pysqlite3`
  - `langdetect`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/leventguel/mein_erstes_projekt.git
   cd your-repo

2. Install dependencies (if any are external to Python's standard library):
   pip install -r requirements.txt

3. Run the application:
   python main.py

### Usage

When starting the application, you can choose between:

    CLI Mode: Manage poems through the command-line interface.
    GUI Mode: Interact with the application through an intuitive graphical interface.

In the GUI mode, you can:

    Add a new poem via a popup form.
    View all stored poems in a scrollable, dynamically styled window.
    Import poems from external files.
    Change the font and size settings.

### Roadmap
Features to Implement

    Delete poems directly via the GUI or CLI.
    Improved GUI styling for better user experience.
    Export poems to a file.
    Cloud storage integration for poem data.

Known Issues

    Line-wrapping in the GUI version may slightly differ from CLI text rendering.
    Limited language support (extendable via MENU_TRANSLATIONS).

### Contributing

Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request.

### License

This project is licensed under the MIT License.

### Acknowledgments

Special thanks to everyone who helped refine and debug the project during its development. 😊