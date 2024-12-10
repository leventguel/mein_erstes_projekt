# Aufgabenblatt Python mit Datenbanken
# Aufgabe 7
import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
def connect_db():
    return sqlite3.connect("todo.db")

# Tabelle für To-Do-Listen erstellen
def create_table():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS aufgaben (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titel TEXT NOT NULL,
                status TEXT DEFAULT 'offen' CHECK(status IN ('offen', 'erledigt'))
            );
        ''')
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()

# Funktion zum Hinzufügen einer neuen Aufgabe
def add_task():
    titel = input("Geben Sie den Titel der Aufgabe ein: ").strip()
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO aufgaben (titel, status) VALUES (?, ?);", (titel, "offen"))
        print("Aufgabe erfolgreich hinzugefügt.")
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()

# Funktion zum Anzeigen aller Aufgaben
def show_tasks():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM aufgaben;")
        tasks = cursor.fetchall()
        if tasks:
            print("\nAlle Aufgaben:")
            for task in tasks:
                print(f"ID: {task[0]}, Titel: {task[1]}, Status: {task[2]}")
        else:
            print("Keine Aufgaben in der Liste.")
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.close()

# Funktion zum Markieren einer Aufgabe als erledigt
def mark_task_done():
    try:
        task_id = int(input("Geben Sie die ID der Aufgabe ein, die als erledigt markiert werden soll: ").strip())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE aufgaben SET status = 'erledigt' WHERE id = ?;", (task_id,))
        if cursor.rowcount > 0:
            print("Aufgabe erfolgreich als erledigt markiert.")
        else:
            print("Keine Aufgabe mit dieser ID gefunden.")
    except ValueError:
        print("Bitte geben Sie eine gültige ID ein.")
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()

# Funktion zum Löschen einer Aufgabe
def delete_task():
    try:
        task_id = int(input("Geben Sie die ID der Aufgabe ein, die gelöscht werden soll: ").strip())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM aufgaben WHERE id = ?;", (task_id,))
        if cursor.rowcount > 0:
            print("Aufgabe erfolgreich gelöscht.")
        else:
            print("Keine Aufgabe mit dieser ID gefunden.")
    except ValueError:
        print("Bitte geben Sie eine gültige ID ein.")
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()

# Hauptmenü der Anwendung
def main():
    create_table()
    print("Willkommen zur To-Do-Listen-Anwendung!")
    while True:
        print("""
1: Aufgabe hinzufügen
2: Alle Aufgaben anzeigen
3: Aufgabe als erledigt markieren
4: Aufgabe löschen
5: Beenden
        """)
        option = input("Wählen Sie eine Option (1-5): ").strip()

        if option == "1":
            add_task()
        elif option == "2":
            show_tasks()
        elif option == "3":
            mark_task_done()
        elif option == "4":
            delete_task()
        elif option == "5":
            print("Programm beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Auswahl. Bitte wählen Sie eine Option von 1 bis 5.")

if __name__ == "__main__":
    main()
