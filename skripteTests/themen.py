import importlib
import sys

from skripte.erstellen import *
from funktionen import get_aufgaben

import django

django.setup()
from aufgaben.models import Themen


identifier = sys.argv[1]
uuid = sys.argv[2]
probe = True if sys.argv[-2] == 'True' else False
Art = 'Probe' if probe else 'Test'

Titel = identifier
Fach = Themen.objects.get(name=identifier).fach


# Aufgaben
alle_aufgaben = get_aufgaben(identifier)
alphabet = string.ascii_lowercase

brauch_aufg = []
brauch_teilaufg = []
temp = sys.argv[-1][1:-1].replace(r"'", '').split(', ')
for i in temp:
    if '.' in i:
        brauch_teilaufg.append(i)
    else:
        brauch_aufg.append(i)

selected = []
for aufgabe in alle_aufgaben:
    temp_selected = []
    if aufgabe[0] in brauch_aufg:
        temp_selected.append([aufgabe[0], aufgabe[1]])
        temp_teilaufg = []
        for teilaufgabe in aufgabe[3]:
            if teilaufgabe[0] in brauch_teilaufg:
                temp_teilaufg.append(alphabet[int(teilaufgabe[0][-1])-1])
            else:
                continue
        temp_selected.append(temp_teilaufg)
    else:
        continue
    selected.append(temp_selected)


liste_punkte = ['Punkte']
liste_bez = ['Aufgabe']

aufgaben_seite1 = []

module = importlib.import_module(f'Aufgaben.{Themen.objects.get(name=identifier).stufe}_{identifier}')

for i, aufgabe in enumerate(selected, start=1):
    func = getattr(module, aufgabe[0][1])
    if len(aufgabe[1]) != 0:
        aufgaben_seite1.append(func(i, aufgabe[1]))
    else:
        aufgaben_seite1.append(func(i))

for element in aufgaben_seite1:
    liste_bez.extend(element[5])
    liste_punkte.extend(element[4])

liste_seiten = [seite(aufgaben_seite1)]

schule, schulart, Kurs, Klasse, Lehrer, Titel, datum_delta = str, str, str, str, str, str, 0
angaben = [schule, schulart, Kurs, Fach, Klasse, Lehrer, Art, Titel, datum_delta, liste_bez, liste_punkte, False,
           identifier, uuid]

args = sys.argv[3:-2]
for arg in args:
    key, value = arg.split(':')
    angaben[int(key)] = str(value) if value != '' else angaben[int(key)]

test_erzeugen(liste_seiten, angaben, probe=probe)
