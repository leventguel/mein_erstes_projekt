import sqlite3

# Funktion zur Verbindung mit der SQLite-Datenbank
def connect_db():
    conn = sqlite3.connect("main.db")
    return conn

# Funktion zur Erstellung der Tabelle
def create_benutzer():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "Benutzer" (
                "Id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                "name" TEXT NOT NULL UNIQUE CHECK(length(name) <= 100),
                "email" TEXT UNIQUE CHECK(length(email) <= 255),
                "LebensAlter" INTEGER NOT NULL
            );
        ''')
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()

# Funktion zum Hinzufügen von Einträgen (statisch), mit Überprüfung auf Duplikate
def add_benutzer_entries():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Versuche, Einträge nur hinzuzufügen, wenn sie nicht bereits existieren
        cursor.execute('''
            INSERT OR IGNORE INTO Benutzer ("name", "email", "LebensAlter")
            VALUES
                ('Hans Zimmermann', 'hans@zimmer.de', 55),
                ('Johan Teufel', 'john@teufel.com', 33),
                ('Greta Gerwisch', 'gerwisch.greta@meisterkuechen.de', 26);
        ''')
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()

# Aufgabe 2
# Funktion zum Abrufen von Einträgen
# Aufgabe 5
# mit einem optionalen Filterkriterium
def get_benutzer(filter_criteria="LebensAlter > 25"):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Wenn der Filter leer ist, verwenden wir den Standardfilter
        if filter_criteria == "":
            filter_criteria = "LebensAlter > 25"

        # Überprüfen, ob das Filterkriterium gültig ist (z.B. keine unbekannten Spalten oder Operatoren)
        allowed_columns = ['LebensAlter', 'name', 'email']
        allowed_operators = ['>', '<', '=', '>=', '<=']

        # Aufteilen der Kriterien in einzelne Teile (z.B. 'LebensAlter > 25')
        parts = filter_criteria.split()

        if len(parts) != 3:
            print("Ungültiges Kriterium. Bitte verwenden Sie das Format 'Spalte Operator Wert'.")
            return

        column, operator, value = parts

        # Überprüfen, ob Spalte und Operator gültig sind
        if column not in allowed_columns or operator not in allowed_operators:
            print("Ungültiges Kriterium. Erlaubte Spalten: 'LebensAlter', 'name', 'email'. Erlaubte Operatoren: '>', '<', '=', '>=', '<='.")
            return

        # Wenn der Wert eine Zahl ist, als Zahl behandeln (z.B. LebensAlter > 25)
        if value.isdigit():
            value = int(value)
            query = f"SELECT * FROM Benutzer WHERE {column} {operator} ?;"
            cursor.execute(query, (value,))
        else:
            # Wenn der Wert ein String ist, sollte er in einfache Anführungszeichen gesetzt werden (z.B. 'Greta')
            query = f"SELECT * FROM Benutzer WHERE {column} {operator} ?;"
            cursor.execute(query, (value,))

        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print(f"Keine Benutzer gefunden, die dem Kriterium '{filter_criteria}' entsprechen.")

    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.close()


# Aufgabe 3
# Eingabe validierung
def validate_name(name_input):
    if len(name_input) > 100:
        return "Der Name darf maximal 100 Zeichen lang sein."
    elif not name_input:
        return "Der Name darf nicht leer sein."
    return None  # Kein Fehler

def validate_email(email_input):
    if len(email_input) > 255:
        return "Die E-Mail darf maximal 255 Zeichen lang sein."
    elif not email_input:
        return "Die E-Mail darf nicht leer sein."
    elif "@" not in email_input or email_input.count("@") != 1:
        return "Ungültige E-Mail-Adresse. Es muss genau ein '@' enthalten sein."
    elif "." not in email_input.split("@")[1]:
        return "Ungültige E-Mail-Adresse. Der Domain-Teil muss einen Punkt enthalten (z. B. '.com')."
    elif email_input.startswith("@") or email_input.endswith("@"):
        return "Ungültige E-Mail-Adresse. Das '@' darf nicht am Anfang oder Ende stehen."
    return None  # Kein Fehler

def validate_lebensalter(lebensalter_input):
    try:
        lebensalter = int(lebensalter_input)
        if lebensalter < 0:
            return "Das LebensAlter darf nicht negativ sein."
        return lebensalter  # Gültiges Alter zurückgeben
    except ValueError:
        return "Bitte geben Sie eine gültige Zahl für das LebensAlter ein."

# Funktion, um die Benutzereingaben zu sammeln (interaktive Abfrage)
def input_user_data():
    print("Bitte geben Sie die folgenden Informationen ein:")
    name, email, LebensAlter = None, None, None

    while not (name and email and LebensAlter is not None):
        if not name:
            name_input = input("Name: ").strip()
            error = validate_name(name_input)
            if error:
                print(error)
            else:
                name = name_input

        if not email:
            email_input = input("E-Mail: ").strip()
            error = validate_email(email_input)
            if error:
                print(error)
            else:
                email = email_input

        if LebensAlter is None:
            lebensalter_input = input("LebensAlter: ").strip()
            result = validate_lebensalter(lebensalter_input)
            if isinstance(result, str):  # Fehlernachricht
                print(result)
            else:
                LebensAlter = result

    return name, email, LebensAlter

# Funktion zum Einfügen von Benutzerdaten (interaktiv) mit Überprüfung auf Duplikate
def add_benutzer(name, email, LebensAlter):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Überprüfen, ob die E-Mail bereits existiert
        cursor.execute('''
            SELECT * FROM Benutzer WHERE email = ?;
        ''', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            print(f"Die E-Mail-Adresse '{email}' ist bereits in der Datenbank vorhanden. Bitte verwenden Sie eine andere E-Mail.")
        else:
            cursor.execute('''
                INSERT INTO Benutzer ("name", "email", "LebensAlter")
                VALUES (?, ?, ?);
            ''', (name, email, LebensAlter))
            conn.commit()
            print(f"Benutzer {name} erfolgreich hinzugefügt.")
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.close()

# Aufgabe 4
# Funktion, um Benutzer zur Eingabe zu bitten falls die id bekannt ist
def input_update_data_by_id():
    while True:
        try:
            user_id = int(input("Bitte geben Sie die Id des Benutzers ein, dessen E-Mail Sie ändern möchten: "))
            break
        except ValueError:
            print("Die Id muss eine Zahl sein. Bitte erneut versuchen.")

    new_email = input("Bitte geben Sie die neue E-Mail-Adresse ein: ")
    return user_id, new_email

# Funktion zum Aktualisieren der E-Mail anhand der ID
def update_email_by_id(user_id, new_email):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Überprüfen, ob die neue E-Mail bereits in der Datenbank existiert
        cursor.execute('''
            SELECT * FROM Benutzer WHERE email = ?;
        ''', (new_email,))
        existing_user = cursor.fetchone()

        if existing_user:
            print(f"Die E-Mail-Adresse '{new_email}' ist bereits in der Datenbank vorhanden. Bitte verwenden Sie eine andere E-Mail.")
        else:
            cursor.execute('''
                UPDATE Benutzer
                SET email = ?
                WHERE Id = ?;
            ''', (new_email, user_id))
            conn.commit()

            if cursor.rowcount == 0:
                print(f"Kein Benutzer mit der ID {user_id} gefunden.")
            else:
                print(f"E-Mail erfolgreich auf {new_email} aktualisiert.")
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.close()


# Funktion, um Benutzer zur Eingabe zu bitten falls die id unbekannt ist
def input_update_data_by_name():
    name = input("Bitte geben Sie den Namen des Benutzers ein, dessen E-Mail Sie ändern möchten: ")
    new_email = input("Bitte geben Sie die neue E-Mail-Adresse ein: ")
    return name, new_email

# Funktion zum Aktualisieren der E-Mail falls die id unbekannt ist
# Funktion zum Aktualisieren der E-Mail anhand des Namens
def update_email_by_name(name, new_email):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Überprüfen, ob die neue E-Mail bereits in der Datenbank existiert
        cursor.execute('''
            SELECT * FROM Benutzer WHERE email = ?;
        ''', (new_email,))
        existing_user = cursor.fetchone()

        if existing_user:
            print(f"Die E-Mail-Adresse '{new_email}' ist bereits in der Datenbank vorhanden. Bitte verwenden Sie eine andere E-Mail.")
        else:
            # Teilstring-Suche nach Namen (LIKE-Operator)
            cursor.execute('''
                UPDATE Benutzer
                SET email = ?
                WHERE name LIKE ?;
            ''', (new_email, '%' + name + '%'))  # '%' erlaubt Teilstring-Suche
            conn.commit()

            if cursor.rowcount == 0:
                print(f"Kein Benutzer mit einem Namen, der '{name}' enthält, gefunden.")
            else:
                print(f"E-Mail für Benutzer mit Namen '{name}' erfolgreich auf '{new_email}' aktualisiert.")
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.close()

# Aufgabe 6
# Funktion, um Benutzer nach Namen zu suchen und die Informationen anzuzeigen
def search_benutzer_by_name():
    name = input("Bitte geben Sie den Namen des Benutzers ein, den Sie suchen möchten: ")
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Suchen nach dem Namen, hier auch Teilstrings erlaubt (LIKE-Operator)
        cursor.execute('''
            SELECT * FROM Benutzer WHERE name LIKE ?;
        ''', ('%' + name + '%',))  # '%' erlaubt eine unscharfe Suche

        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, E-Mail: {row[2]}, LebensAlter: {row[3]}")
        else:
            print(f"Kein Benutzer mit dem Namen '{name}' gefunden.")
    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankoperation: {e}")
    finally:
        if conn:
            conn.close()


# Hauptmenü
def main():
    create_benutzer()
    add_benutzer_entries()

    print("Willkommen zum Benutzerprogramm!")
    while True:
        # Mehrzeilige Eingabeaufforderung für das Menü
        option = input("""
1: Neuen Benutzer hinzufügen
2: E-Mail eines bestehenden Benutzers ändern
3: Alle Benutzer nach einem Kriterium anzeigen
4: Benutzer nach Namen suchen
Wählen Sie eine Option (1/2/3/4): """).strip()

        if option == '1':  # Neuen Benutzer hinzufügen
            name, email, LebensAlter = input_user_data()
            add_benutzer(name, email, LebensAlter)
        elif option == '2':  # E-Mail eines bestehenden Benutzers ändern
            bekannt = input("ID des Benutzers bekannt? (j/n): ").lower()
            if bekannt == "j":  # ID bekannt
                user_id, new_email = input_update_data_by_id()  # Eingabe der ID und neuen E-Mail
                update_email_by_id(user_id, new_email)  # E-Mail mit der ID aktualisieren
            else:  # ID unbekannt, stattdessen Name verwenden
                name, new_email = input_update_data_by_name()  # Eingabe des Namens und der neuen E-Mail
                update_email_by_name(name, new_email)  # E-Mail mit dem Namen aktualisieren
        elif option == '3':  # Benutzer nach Kriterium anzeigen
            filter_criteria = input("Filterkriterium (z.B. 'LebensAlter > 30') oder Enter für Standard (LebensAlter > 25): ").strip()
            if not filter_criteria:
                filter_criteria = "LebensAlter > 25"
            get_benutzer(filter_criteria)
        elif option=='4':  # Benutzer nach Namen suchen
            search_benutzer_by_name()  # Neue Funktion zum Suchen nach Benutzern
        else:
            print("Ungültige Auswahl. Bitte 1, 2, 3 oder 4 wählen.")
            continue

        # Möchte der Benutzer noch einen weiteren Vorgang durchführen?
        weitere = input("Weiteren Vorgang durchführen? (j/n): ").lower()
        if weitere != "j":
            print("Programm beendet. Auf Wiedersehen!")
            break

if __name__ == "__main__":
    main()
