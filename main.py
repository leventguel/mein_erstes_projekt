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

def eingabe_beispiel ():
	meine_globale_variable = input("Bitte gib eine Zahl ein!: ")
	print("lokal ausgedruckt: ", meine_globale_variable)
	return "Rückgabewert: " + meine_globale_variable

print("Die Globale ist immernoch: ", meine_globale_variable) # hier wird 0 zurückgegeben
print(eingabe_beispiel())
