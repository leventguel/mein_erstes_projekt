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

print("Typ von vowels: ", type(vowels))

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Summe: " + str(sum(nums)))
print("Maximum: " + str(max(nums)))
print("Minimum: " + str(min(nums)))

durcheinander = ["c", "d", "b", "g", "a", "m"]

sortiert = sorted(durcheinander)

print("Sortiert: ", sortiert)

# Eingabe verarbeiten
konvertiert = int(input("Bitte nur Ganze Zahl eingeben: "))
print("Konvertiert:", konvertiert)
print("Ist es eine Ganze Zahl ?: Antwort:", isinstance(konvertiert, int))

konvertiert2 = int(float(input("Geben Sie bitte eine Zahl ein: ")))
print("Hier ist kein Eingabefehler möglich")
print("Konvertiert:", konvertiert2)
