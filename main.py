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

# Aufgabe 2

def gerade_ungerade (zahl):
	if zahl % 2 == 0:
		antwort = "gerade"
	else:
		antwort = "ungerade"
	return antwort

eingabe_Aufforderung = int(float(input("Bitte geben Sie eine Zahl ein: ")))
print(f'Die Zahl {eingabe_Aufforderung} ist {gerade_ungerade(eingabe_Aufforderung)}')

# Aufgabe 2.1
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

print(f'Die Zahl {vergleich} ist {überprüfe_Nummer(vergleich)} {Ziel}')


