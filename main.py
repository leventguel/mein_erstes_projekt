""" Literale """
123
22.01
"Hello"

True
False

[1,2,3,"a","b"]

""" Kommentare und Bezeicher """

meine_globale_variable = 0 # eine globale variable

print("Die Globale: {}".format(meine_globale_variable))

def meine_beispiel_funktion ():
	meine_globale_variable = 1
	print("Die lokale ausgedruckte: ", meine_globale_variable)
	return meine_globale_variable

print("Die zurückgegebene: {}".format(meine_beispiel_funktion()))

def anderes_beispiel ():
	meine_globale_variable = 3
	print("lokal ausgedruckt: ", meine_globale_variable)
	return "Rückgabewert: " + str(meine_globale_variable)

print("Die Globale ist immer noch: ", meine_globale_variable) # hier wird 0 zurückgegeben
print(anderes_beispiel())

# Verschachtelte Namensräume
def umschliessende ():
	hallo = 2
	print(hallo)
	def eingeschlossene ():
		nonlocal hallo
		hallo = 3
		print(hallo)
	eingeschlossene()

umschliessende()

# Built-in Funktionen verwenden

msg = "Die Kunst des Lebens besteht nicht darin, auf die Sonne zu warten, sondern im Regen zu tanzen."

print(len(msg))

vowels = ["a","e","i","o","u","ä","ö","ü"]

# Extraktion des Typs in <class 'list'>
print("Typ von vowels: ", str(type(vowels)).split("'")[1])

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Summe: " + str(sum(nums)))
print("Maximum: " + str(max(nums)))
print("Minimum: " + str(min(nums)))

durcheinander = ["c", "d", "b", "g", "a", "m"]

sortiert = sorted(durcheinander)

print("Sortiert: ", sortiert)

# Eingabe verarbeiten
print("Bitte nur Ganze Zahl eingeben, sonst ist eine Fehlerausgabe möglich!")
konvertiert = int(input("Eingabe: "))
print("Konvertiert:", konvertiert)
print("Ist es eine Ganze Zahl ?: Antwort:", isinstance(konvertiert, int))

konvertiert2 = int(float(input("Geben Sie bitte eine Zahl ein: ")))
print("Hier ist kein Eingabefehler möglich")
print("Konvertiert:", konvertiert2)
print("Ist es eine Ganze Zahl ?: Antwort:", isinstance(konvertiert2, int))

# Teil 2 des Aufgabenblatts
# Aufgabe 1
startwert = 10
zwischenwert = startwert + 5
Endwert = zwischenwert * 2
print(f'\nStartwert: {startwert} \nZwischenwert: {zwischenwert} \nEndwert: {Endwert}')

# Aufgabe 2.1

def gerade_ungerade (zahl):
	if zahl % 2 == 0:
		antwort = "gerade"
	else:
		antwort = "ungerade"
	return antwort

eingabe_Aufforderung = int(float(input("Bitte geben Sie eine Zahl ein: ")))
print(f'Die Zahl {eingabe_Aufforderung} ist {gerade_ungerade(eingabe_Aufforderung)}')

# Aufgabe 2.2
Ziel = 100
def überprüfe_Nummer (zahl, vergleichszahl=Ziel):
	if zahl > vergleichszahl:
		antwort = "größer"
	elif zahl < vergleichszahl:
		antwort = "kleiner"
	elif zahl == vergleichszahl:
		antwort = "gleich"
	return antwort

vergleich = 99
vergleich2 = 101

print(f'Die Zahl {vergleich} ist {überprüfe_Nummer(vergleich)} {Ziel}')
print(f'Die Zahl {vergleich2} ist {überprüfe_Nummer(vergleich2)} {Ziel}')
print(f'Die Zahl {Ziel} ist {überprüfe_Nummer(Ziel)} {Ziel}')

# Aufgabe 2.3
def check_password(password):
    # Fehlerliste
    errors = []

    # Länge prüfen
    if len(password) < 8:
        errors.append("Das Passwort muss mindestens 8 Zeichen lang sein.")

    # Prüfen, ob das Passwort nicht mit einer Zahl beginnt
    if password[0].isdigit():
        errors.append("Das Passwort darf nicht mit einer Zahl beginnen.")

    # Sonderzeichen prüfen (mindestens zwei)
    special_characters = "!@#$%^&*(),.?\":{}|<>"
    special_count = sum(1 for char in password if char in special_characters)
    if special_count < 2:
        errors.append("Das Passwort muss mindestens zwei Sonderzeichen enthalten.")

    # Kombination aus Buchstaben und Sonderzeichen prüfen
    has_letter = any(char.isalpha() for char in password)
    has_special = any(char in special_characters for char in password)
    if not has_letter or not has_special:
        errors.append("Das Passwort muss Buchstaben und Sonderzeichen kombinieren.")

    # Rückmeldung geben
    if errors:
        return False, errors
    return True, ["Das Passwort erfüllt alle Kriterien."]

# Benutzer auffordern
password = input("Bitte geben Sie ein Passwort ein: ")
valid, messages = check_password(password)

# Ergebnisse anzeigen
if valid:
    print(messages[0])
else:
    print("Das Passwort ist ungültig:")
    for message in messages:
        print(f"- {message}")


try:
    from getpass import getpass  # Versuch, getpass zu nutzen
except ImportError:
    getpass = None

import os
if os.name == "nt":
    import msvcrt

    def hidden_input_windows(prompt=""):
        if getpass:
            print("DEBUG: Verwende getpass für die Passworteingabe.")
            return getpass(prompt)
        print(prompt, end="", flush=True)
        password = ""
        while True:
            print("DEBUG: Warten auf Eingabe (msvcrt)...")
            char = msvcrt.getch()
            print(f"DEBUG: Eingabe erhalten: {char}")
            if char in {b"\r", b"\n"}:  # Enter-Taste
                print()
                break
            elif char in {b"\x08", b"\x7f"}:  # Backspace
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            else:
                password += char.decode("utf-8")
                print("*", end="", flush=True)
        return password

    hidden_input = hidden_input_windows

else:
    import sys
    import tty
    import termios

    def hidden_input_unix(prompt=""):
        if getpass:
            print("DEBUG: Verwende getpass für die Passworteingabe.")
            return getpass(prompt)
        print(prompt, end="", flush=True)
        password = ""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                print("DEBUG: Warten auf Eingabe (Unix)...")
                char = sys.stdin.read(1)
                print(f"DEBUG: Eingabe erhalten: {char}")
                if char in ("\n", "\r"):  # Enter-Taste
                    print()
                    break
                elif char in ("\x08", "\x7f"):  # Backspace
                    if password:
                        password = password[:-1]
                        print("\b \b", end="", flush=True)
                else:
                    password += char
                    print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return password

    hidden_input = hidden_input_unix

# Test
password = hidden_input("Bitte geben Sie Ihr Passwort ein: ")
print(f"Eingegebenes Passwort: {password}")

# Aufgabe 2.4
def zwischen(zahl, start, end):
    if zahl > start and zahl < end:
        antwort = "Ja"
    else:
        antwort = "Nein"
    return antwort

print(f'Ist 50 zwischen 100 und 200 ? {zwischen(50, 100, 200)}')
print(f'Ist 50 zwischen -100 und 100 ? {zwischen(50, -100, 100)}')
print(f'Ist 50.5 zwischen 50 und 51 ? {zwischen(50.5, 50, 51)}')

# Aufgabe 2.5
def alt_genug_zum_fahren():
    alter = int(float(input("Bitte geben Sie ihr Alter ein: ")))
    if alter >= 18:
        antwort = "Du darfst Auto fahren"
    elif 16 <= alter < 18:
        antwort = "Du darfst einen Führerschein machen"
    elif alter < 16:
        antwort = "Du bist zu jung für den Führerschein"
    return antwort

print(f'Bin ich alt genug zum Autofahren: {alt_genug_zum_fahren()}')

# Aufgabe 2.6
def gleich_groß():
    erste_Zahl = float(input("Bitte gib die erste Zahl ein: "))
    zweite_Zahl = float(input("Bitte gib die zweite Zahl ein: "))

    if (erste_Zahl + zweite_Zahl) % 2 == 0:
        Summe = "gerade"
    else:
        Summe = "ungerade"

    if erste_Zahl == zweite_Zahl:
        antwort = "gleich"
        print(f'Die Zahlen sind {antwort} und die Summe ist {Summe}')
    elif erste_Zahl != zweite_Zahl:
        antwort = max(erste_Zahl, zweite_Zahl)
        print(f'{antwort} ist die größere und die Summe ist {Summe}')

gleich_groß()

# Aufgabe 3
Zitate = ["Carpe diem", "Alea iacta est", "Sapere aude", "Non scholae, sed vitae discimus",
"Amor vincit omnia", "Errare humanum est","Festina lente", "Per aspera ad astra "]
Vorname = "Levent"
Nachname = "Guel"
Ausbildung = "Fachinformatik in Richtung Anwendungsentwicklung"

def index():
    from random import randint
    return randint(0, len(Zitate) - 1)

def info():
    print(f"{Vorname} {Nachname} ist in der Ausbildung für {Ausbildung}\nZitat: {Zitate[index()]}")

info()

# Aufgabe 4
ein_Tabulator = "\t"
ein_Zeilenumbruch = "\n"
print(f"Hallo Tabulator:{ein_Tabulator}mit{ein_Zeilenumbruch}Zeilenumbruch")

# Aufgabe 5

Name = input("Bitte geben Sie ihren Namen ein: ")
Alter = int(input("Bitte geben Sie ihr Alter ein: "))
Beruf = input("Bitte geben Sie ihr Beruf ein: ")

print(f'Hallo {Name} vom Beruf {Beruf}')

# Aufgabe 6

def check_Eingabe():
    Eingabe = input("Bitte geben Sie eine Zahl ein: ")
    valid = Eingabe.isdigit()

    while not valid:
        Eingabe = input("Bitte geben Sie die Zahl erneut ein: ")
        valid = Eingabe.isdigit()
        if not valid:
            print("Leider ist ihre Eingabe ungültig, versuchen Sie es erneut!")
        else:
            break

    print("Ok, Ihre Eingabe ist gültig und ist nun vermerkt!")

check_Eingabe()

# Aufgabe 7.1
Zahl = 3
Gleitkommazahl = 3.1415
Text = "Dies ist ein Text"
Wahrheitswert = True or False

# Aufgabe 7.2 ugly version
print("ugly version\n")
print(f'''\nTyp von Zahl ist:\t\t\t"{str(type(Zahl)).split("'")[1]}" 
Typ von Gleitkommazahl ist:\t"{str(type(Gleitkommazahl)).split("'")[1]}" 
Typ von Text ist:\t\t\t"{str(type(Text)).split("'")[1]}" 
Typ von Wahrheitswert ist:\t"{str(type(Wahrheitswert)).split("'")[1]}"''')

# Aufgabe 7.2 better version
print("elegant version\n")
print(f'''
{"Typ von Zahl ist:":<30} {type(Zahl).__name__}
{"Typ von Gleitkommazahl ist:":<30} {type(Gleitkommazahl).__name__}
{"Typ von Text ist:":<30} {type(Text).__name__}
{"Typ von Wahrheitswert ist:":<30} {type(Wahrheitswert).__name__}
''')

# Aufgabe 8
Zahl = 8
Gleitkommazahl = float(Zahl)
Gleitkommazahl2 = 3.14
Zahl2 = int(Gleitkommazahl2)
String1 = str(Gleitkommazahl)
String2 = str(Zahl2)
Zahl3 = int(String2)
print(f"\n{Zahl,Gleitkommazahl,Gleitkommazahl2, Zahl2, String1, String2, Zahl3}")

# Aufgabe 9

def Abfrage():
    try:
        zahl_Eingabe = input("Bitte geben Sie eine Zahl ein: ")
        valid = zahl_Eingabe.isdigit()

        if not valid:
            print("Ihre Eingabe ist ungültig")
        else:
            zahl = int(zahl_Eingabe)
            return zahl/2

    except Exeption as e:
        print(e)

print(Abfrage())

# Aufgabenzettel teil 3

# Aufgabe 1
läufer = 1
end = 10
while läufer < end:
    print(läufer)
    läufer += 1

def zähler_liste(end, start=0):
    läufer = start
    antwort = []
    while läufer < end:
        antwort.append(läufer)
        läufer +=1
    return antwort

print(zähler_liste(10))

# Aufgabe 2
def Summe():
    Summe = 0
    while True:
        zahl = input("Bitte geben Sie eine Zahl ein: ")
        if zahl.isdigit:
            Summe += float(zahl)
        else:
            "Leider ist ihre Eingabe keine Zahl"
        if zahl == "0":
            break
    print("Die Summe ist: ")
    return Summe

# Aufgabe 3

def überprüfe_passwort():
    gesichertes_passwort = "@3rl!abc"
    passwort_eingabe = input("Bitte password eingeben: ")
    print(f"Hinweis: {check_password(passwort_eingabe)[1][0]}")
    while passwort_eingabe != gesichertes_passwort:
        passwort_eingabe = input("Bitte geben Sie das richtige Passwort ein!: ")
        print(f"Hinweis: {check_password(passwort_eingabe)[1][0]}")
        print("Erfolg! ihr passwort ist validiert!")

überprüfe_passwort()

# Aufgabe 4

for i in range(1,11):
    print(i)

for i in range(10):
    print(i+1)

def zähler_0_basiert(zahl): # 0 basierter zähler
    for i in range(zahl):
        print(i)

zähler_0_basiert(10)

def zähler_1_basiert(zahl): # 1 basierter zähler
    for i in range(zahl):
        print(i+1)

zähler_1_basiert(10)

# Aufgabe 5
for i in range(21):
    if i % 2 == 0:
        print(i)

for i in range(21):
    if i % 5 == 0:
        print(i)

def gerade_zahlen(bis):
    for i in range(bis+1):
        if i % 2 == 0:
            print(i)

gerade_zahlen(20)

def jede_5te(bis):
    for i in range(bis+1):
        if i % 5 == 0:
            print(i)

jede_5te(20)

# Aufgabe 6

def rechteck_mit_sternen(row, col, char="*"):
    for i in range(row):
        print(char * col)

rechteck_mit_sternen(3, 7, "#")

# Aufgabe 7
for i in range(10, 0, -1):
    print(i)

läufer = 10
end = 0
while läufer > end:
    print(läufer)
    läufer -= 1

def rückwärts_zähler1(von, bis=0):
    for i in range(von, bis, -1):
        print(i)

def rückwärts_zähler2(von, bis=0):
    läufer = von
    end = bis
    while läufer > end:
        print(läufer)
        läufer -= 1

def while_generator(start):
    while start > 0:
        yield start
        start -= 1

result = while_generator(10)
list(result)

# Aufgabe 8

mList = ["Anna", "Max", "Tom", "Lisa"]

mList.append("Marie")

mList.remove("Tom")

len(mList)
