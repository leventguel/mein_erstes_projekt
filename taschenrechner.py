# Aufgabenblatt Python Projekte
# Projekt 1 Taschenrechner

import math

# Liste zur Speicherung der Berechnungen
history = []


# Funktion zur Addition
def add(x, y):
    return x + y


# Funktion zur Subtraktion
def subtract(x, y):
    return x - y


# Funktion zur Multiplikation
def multiply(x, y):
    return x * y


# Funktion zur Division
def divide(x, y):
    if y==0:
        return "Fehler: Division durch Null ist nicht erlaubt."
    return x / y


# Funktion zum Potenzieren
def power(x, y):
    return x ** y


# Funktion zur Quadratwurzel
def square_root(x):
    if x < 0:
        return "Fehler: Negative Zahlen haben keine reale Quadratwurzel."
    return math.sqrt(x)


# Funktion zur Prozentberechnung
def percentage(x, y):
    return (x * y) / 100


# Funktion zur Anzeige der Berechnungen aus der Historie
def show_history():
    if not history:
        print("Keine Berechnungen bisher durchgeführt.")
    else:
        print("Berechnungen History:")
        for index, entry in enumerate(history, 1):
            print(f"{index}. {entry}")


# Funktion zur Eingabe von Zahlen mit Fehlerbehandlung
def get_number(prompt):
    while True:
        try:
            number = float(input(prompt))
            return number
        except ValueError:
            print("Ungültige Eingabe! Bitte eine Zahl eingeben.")


# Hauptfunktion für das Menü
def main():
    while True:
        print("\n--- Taschenrechner ---")
        print("1. Addition")
        print("2. Subtraktion")
        print("3. Multiplikation")
        print("4. Division")
        print("5. Potenzieren")
        print("6. Quadratwurzel")
        print("7. Prozentrechnung")
        print("8. Berechnungen anzeigen (Historie)")
        print("9. Beenden")

        choice = input("Wählen Sie eine Option (1/2/3/4/5/6/7/8/9): ")

        if choice=='1':
            num1 = get_number("Geben Sie die erste Zahl ein: ")
            num2 = get_number("Geben Sie die zweite Zahl ein: ")
            result = add(num1, num2)
            history.append(f"{num1} + {num2} = {result}")
            print(f"Ergebnis: {result}")

        elif choice=='2':
            num1 = get_number("Geben Sie die erste Zahl ein: ")
            num2 = get_number("Geben Sie die zweite Zahl ein: ")
            result = subtract(num1, num2)
            history.append(f"{num1} - {num2} = {result}")
            print(f"Ergebnis: {result}")

        elif choice=='3':
            num1 = get_number("Geben Sie die erste Zahl ein: ")
            num2 = get_number("Geben Sie die zweite Zahl ein: ")
            result = multiply(num1, num2)
            history.append(f"{num1} * {num2} = {result}")
            print(f"Ergebnis: {result}")

        elif choice=='4':
            num1 = get_number("Geben Sie die erste Zahl ein: ")
            num2 = get_number("Geben Sie die zweite Zahl ein: ")
            result = divide(num1, num2)
            history.append(f"{num1} / {num2} = {result}")
            print(f"Ergebnis: {result}")

        elif choice=='5':
            num1 = get_number("Geben Sie die Basiszahl ein: ")
            num2 = get_number("Geben Sie den Exponenten ein: ")
            result = power(num1, num2)
            history.append(f"{num1} ^ {num2} = {result}")
            print(f"Ergebnis: {result}")

        elif choice=='6':
            num1 = get_number("Geben Sie die Zahl ein: ")
            result = square_root(num1)
            history.append(f"√{num1} = {result}")
            print(f"Ergebnis: {result}")

        elif choice=='7':
            num1 = get_number("Geben Sie die Zahl ein: ")
            num2 = get_number("Geben Sie den Prozentsatz ein: ")
            result = percentage(num1, num2)
            history.append(f"{num1} von {num2}% = {result}")
            print(f"Ergebnis: {result}")

        elif choice=='8':
            show_history()

        elif choice=='9':
            print("Programm beendet.")
            break

        else:
            print("Ungültige Auswahl. Bitte wählen Sie eine gültige Option.")


if __name__=="__main__":
    main()
