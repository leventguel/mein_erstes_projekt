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
