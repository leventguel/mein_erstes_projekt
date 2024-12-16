Java Database Operations CLI/GUI

This is a Java-based application that provides database operations with both Command-Line Interface (CLI) and Graphical User Interface (GUI) support. The application allows users to perform operations such as creating a database, inserting data, retrieving data, and deleting entries either through a console or a GUI.

Features

    Create Database: Create a new database.
    Insert Test Data: Insert sample data into the database.
    Retrieve Data: Retrieve and display data from the database in both CLI and GUI formats.
    Delete Entries: Delete entries from the database either by column value or delete all entries.

Prerequisites

    Java 8 or newer: Make sure Java is installed on your system.
    JDBC Database: The application interacts with a database using JDBC. Make sure you have a database connection set up (e.g., MySQL, PostgreSQL).
    Maven: The project uses Maven for dependency management and building.

Getting Started
Clone the repository

git clone <repository-url>
cd <project-directory>

Build the project using Maven

mvn clean install or mvn clean compile

Running the Application

GUI Version

To run the GUI version of the application, simply execute the following:

mvn exec:java "-Dexec.mainClass=lf8.DatabaseOperationsGUI"

or mvn exec:java "-Dexec.mainClass=lf8.DatabaseOperationsGUI" "-DuseGui=False"
/* currently this is not implemented correctly */

The GUI will launch, allowing you to perform operations through buttons and input fields.


CLI Version

If you're running the application in a headless environment or prefer using the command line, the program will default to the CLI mode. You can also specify CLI mode explicitly (if desired) by adjusting the code.

mvn exec:java "-Dexec.mainClass=lf8.TestConnection" for example
/* The arguments have to be quoted like above in powershell for example */

This will run the application in a CLI format where you can view and interact with the database through text outputs.

Usage

Once the application is running, you will be presented with the following options:

GUI Mode:

    Create Database: Click the "Create Database" button to create a new database.
    Insert Test Data: Click the "Insert Test Data" button to insert sample data.
    Retrieve Data: Click the "Retrieve Data" button to fetch and display data from the database in the table.
    New Entry: Click the "New Entry" button to enter new student data.
    Delete Entries: Click the "Delete Entries" button to delete data either by column value or delete all entries.

CLI Mode:

In the CLI version, the data will be displayed in the terminal, and you can perform database operations by choosing the available options in the prompt. (Currently there's no unified CLI Interface).

File Structure:
|--src:
|   |--	main:
|	  |--java:
|	       |--lf8:
|		-a----        13.12.2024     10:49           4149 CombinedDatabaseOperations.java
|		-a----        13.12.2024     12:00           1994 CreateDatabase.java
|		-a----        13.12.2024     10:16           1802 CreateTable.java
|		-a----        16.12.2024     11:36          10053 DatabaseOperationsGUI.java
|		-a----        13.12.2024     10:23            495 DatabaseUtils.java
|		-a----        16.12.2024     10:02           2695 DeleteEntries.java
|		-a----        13.12.2024     14:41            793 InsertData.java
|		-a----        13.12.2024     12:01           3708 InsertTestData.java
|		-a----        13.12.2024     14:35           6387 RetrieveStudents.java
|		-a----        13.12.2024     10:20           1922 TestConnection.java
|--pom.xml
|--README.md

Dependencies

This project uses Maven for dependency management. The following dependencies are used:

    JDBC: Required to interact with databases (mariadb, etc.).
    Swing: For the GUI components.

Contributing

Feel free to fork this repository, create an issue, or submit a pull request if you'd like to contribute.

    -Fork the repository.
    -Create a new branch (git checkout -b feature-name).
    -Make your changes.
    -Commit your changes (git commit -am 'Add feature').
    -Push to the branch (git push origin feature-name). /* This is currently restricted to contributors only */
    -Create a new Pull Request.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgements

    Thanks to the developers of the libraries used in this project.
    Special thanks to Swing for the GUI components.
    Thanks to the open-source community for providing Java Database Connectivity (JDBC).
