import hashlib
import os
import sqlite3
import getpass  # Für sichere Passwortabfrage


# Verbindung zur Datenbank herstellen
def connect_db():
    conn = sqlite3.connect('user.db')
    return conn


# Funktion zum Erstellen der Benutzer-Tabelle in der Datenbank
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Benutzer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            passwort_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Funktion zum Hashen des Passworts mit Salt
def hash_password(password):
    salt = os.urandom(16)  # Erstelle ein zufälliges Salt
    password_salt = password.encode('utf-8') + salt
    hashed_password = hashlib.sha256(password_salt).hexdigest()  # SHA-256-Hash des Passworts + Salt
    return salt, hashed_password


# Funktion zum Überprüfen des Passworts
def check_password(stored_salt, stored_hash, password_to_check):
    password_salt = password_to_check.encode('utf-8') + stored_salt
    hash_to_check = hashlib.sha256(password_salt).hexdigest()
    return hash_to_check == stored_hash


# Benutzer registrieren
def register_user(name, email, password):
    salt, hashed_password = hash_password(password)

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO Benutzer (name, email, passwort_hash, salt)
            VALUES (?, ?, ?, ?)
        ''', (name, email, hashed_password, salt.hex()))
        conn.commit()
        print("Benutzer erfolgreich registriert.")
    except sqlite3.IntegrityError:
        print("Die E-Mail-Adresse ist bereits registriert.")
    finally:
        conn.close()


# Benutzer-Login
def login_user(email, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT passwort_hash, salt FROM Benutzer WHERE email = ?
    ''', (email,))
    user = cursor.fetchone()

    if user:
        stored_hash, stored_salt = user
        stored_salt = bytes.fromhex(stored_salt)  # Umwandlung des gespeicherten Salt in Bytes

        # Überprüfen des Passworts
        if check_password(stored_salt, stored_hash, password):
            print("Login erfolgreich.")
        else:
            print("Falsches Passwort.")
    else:
        print("Benutzer mit dieser E-Mail existiert nicht.")

    conn.close()


# Alle registrierten Benutzer anzeigen
def show_all_users():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, email FROM Benutzer')
    users = cursor.fetchall()

    if users:
        print("Registrierte Benutzer:")
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    else:
        print("Keine registrierten Benutzer gefunden.")

    conn.close()


# Hauptprogramm
def main():
    create_table()  # Sicherstellen, dass die Tabelle existiert

    while True:
        print("""
1. Benutzer registrieren
2. Benutzer-Login
3. Alle registrierten Benutzer anzeigen
4. Beenden
        """)
        choice = input("Wählen Sie eine Option (1/2/3/4): ")

        if choice == '1':
            name = input("Name: ")
            email = input("E-Mail: ")
            password = getpass.getpass("Passwort: ")  # Sichere Passwortabfrage
            register_user(name, email, password)
        elif choice == '2':
            email = input("E-Mail: ")
            password = getpass.getpass("Passwort: ")  # Sichere Passwortabfrage
            login_user(email, password)
        elif choice == '3':
            show_all_users()
        elif choice == '4':
            print("Programm beendet.")
            break
        else:
            print("Ungültige Eingabe. Bitte wählen Sie eine gültige Option.")


if __name__ == "__main__":
    main()
