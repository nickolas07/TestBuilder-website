import datetime
import os
import string
import sympy

from pylatex import (Document, SmallText, LargeText, MediumText, NewPage, Tabular, Alignat, Figure,
                     MultiColumn, Package, HugeText, MultiRow)
from pylatex.utils import bold
from skripteTests.skripte.funktionen import *
from skripteTests.skripte.plotten import *

# Erstellen benötigter Ordner, falls nicht vorhanden
try:
    os.mkdir('pdf')
    os.mkdir('img/temp')
except FileExistsError:
    pass


geometry_options = {"tmargin": "0.2in", "lmargin": "1in", "bmargin": "0.4in", "rmargin": "0.7in"}


# Erstellen der Seiten
def seite(aufgaben):
    Aufgabe = Document(geometry_options=geometry_options)
    Loesung = Document(geometry_options=geometry_options)

    for aufgabe in aufgaben:
        i = 0
        for elements in aufgabe[0]:
            if '~' in elements:
                with Aufgabe.create(Alignat(aligns=1, numbering=False, escape=False)) as agn:
                    agn.append(elements)

            elif 'Figure' in elements:
                with Aufgabe.create(Figure(position='h!')) as graph:
                    graph.add_image(f'../img/temp/{aufgabe[2][i]}', width='250px', placement=None)
                Aufgabe.append(SmallText('Abbildung ' + str(i + 1) + ' \n\n'))
                i += 1

            elif 'Grafik' in elements:
                with Aufgabe.create(Figure(position='h!')) as graph:
                    graph.add_image(f'../img/temp/{aufgabe[2][i]}', width='250px')
                i += 1

            elif 'neueSeite' in elements:
                Aufgabe.append(NewPage())

            elif '3dim_Koordinatensystem' in elements:
                with Aufgabe.create(Figure(position='h!')) as graph:
                    graph.add_image(f'../img/{elements}.png', width='300px')

            else:
                Aufgabe.append(elements)

    for loesung in aufgaben:
        i = 0
        for elements in loesung[1]:
            if '~' in elements:
                with Loesung.create(Alignat(aligns=2, numbering=False, escape=False)) as agn:
                    agn.append(elements)

            elif 'Figure' in elements:
                with Loesung.create(Figure(position='h!')) as graph:
                    graph.add_image(f'../img/temp/{loesung[3][i]}', width='250px')
                i += 1

            elif 'neueSeite' in elements:
                Loesung.append(NewPage())

            elif '3dim_Koordinatensystem' in elements:
                with Loesung.create(Figure(position='h!')) as graph:
                    graph.add_image(f'../img/{elements}.png', width='300px')

            else:
                Loesung.append(elements)

    return Aufgabe, Loesung


# Erzeugung eines Tests
def test_erzeugen(liste_seiten, angaben, probe=False):
    if probe:
        teil = 'Probe'
    else:
        teil = 'Test'
    schule, schulart, Kurs, Fach, Klasse, Lehrer, Art, Titel = \
        (angaben[0], angaben[1], angaben[2], angaben[3], angaben[4], angaben[5], angaben[6], angaben[7])
    datum, liste_bez, liste_punkte = angaben[8], angaben[9], angaben[10]
    schnell, identifier, uuid = angaben[-3], angaben[-2], angaben[-1]

    print(f'\033[38;2;100;141;229m\033[1m{teil}\033[0m')
    Datum = datetime.date.today().strftime('%d.%m.%Y') if datum is not None else datum

    # Erstellung der Tabelle zur Punkteübersicht
    print(liste_punkte)
    Punkte = (sum(liste_punkte[1:]))
    liste_bez.append('Summe')
    liste_punkte.append(Punkte)
    anzahl_spalten = len(liste_punkte)
    liste_ergebnis_z1 = ['erhaltene']
    for p in range(anzahl_spalten - 1):
        liste_ergebnis_z1.append('')
    liste_ergebnis_z2 = ['Punkte']
    for p in range(anzahl_spalten - 1):
        liste_ergebnis_z2.append('')

    spalten = '|'
    for p in liste_punkte:
        spalten += 'c|'

    table2 = Tabular(spalten, row_height=1.2)
    table2.add_hline()
    table2.add_row((MultiColumn(anzahl_spalten, align='|c|', data='Punkteverteilung aller Aufgaben'),))
    table2.add_hline()
    table2.add_row(liste_bez)
    table2.add_hline()
    table2.add_row(liste_punkte)
    table2.add_hline()
    table2.add_row(liste_ergebnis_z1)
    table2.add_row(liste_ergebnis_z2)
    table2.add_hline()

    # der Teil in dem die PDF-Datei erzeugt wird
    @timer
    def Hausaufgabenkontrolle():
        Aufgabe = Document(geometry_options=geometry_options)
        packages(Aufgabe)

        # Kopf erste Seite
        if schnell:
            Aufgabe.append(LargeText(bold(f'{Titel} {uuid} \n\n')))
        else:
            table1 = Tabular('|c|p{2.5cm}|p{2.5cm}|p{2.5cm}|p{2cm}|p{2.5cm}|', row_height=1.2)
            table1.add_row((MultiColumn(6, align='c', data=MediumText(bold(schule))),))
            table1.add_row((MultiColumn(6, align='c', data=SmallText(bold(schulart))),))
            table1.add_hline()
            table1.add_row('Klasse', ' Fach', 'Niveau', 'Lehrkraft', 'Datum', 'Art')
            table1.add_hline()
            if probe:
                table1.add_row(Klasse, Fach, Kurs, Lehrer, Datum, f'{Art}\n {uuid}')
            else:
                table1.add_row(Klasse, Fach, Kurs, Lehrer, Datum, Art)
            table1.add_hline()
            Aufgabe.append(table1)
            Aufgabe.append(' \n\n\n\n')
            Aufgabe.append(LargeText(bold(f' {Titel} \n\n')))

        # hier werden die Aufgaben der einzelnen Seiten an die Liste Aufgabe angehängt
        k = 0
        for element in liste_seiten:
            Aufgabe.extend(element[0])
            Aufgabe.append(NewPage())

        if len(liste_seiten) % 2 == 0:
            Aufgabe.append('für Notizen und Rechnungen:')
            if not schnell:
                Aufgabe.append(NewPage())

        if not schnell:
            Aufgabe.append(LargeText(bold(teil + ' - bearbeitet von:')))

            Aufgabe.append('\n\n')
            Aufgabe.append('\n\n')
            Aufgabe.append(table2)

        Aufgabe.generate_pdf(f'pdf/{identifier} {uuid}', clean_tex=true)

    # Erwartungshorizont
    @timer
    def Erwartungshorizont():
        Loesung = Document(geometry_options=geometry_options)
        packages(Loesung)

        Loesung.append(LargeText(bold(f'Loesung für {teil} - {Titel} {uuid}')))

        # hier werden die Lösungen der einzelnen Seiten an die Liste Aufgabe angehängt
        k = 0
        for element in liste_seiten:
            Loesung.extend(element[1])

        Loesung.append(MediumText(bold(f'insgesamt {Punkte} Punkte')))

        Loesung.generate_pdf(f'pdf/{identifier} {uuid} - Lsg', clean_tex=true)

    # Druck der Seiten
    Hausaufgabenkontrolle()
    Erwartungshorizont()
    del liste_bez[1:]
    del liste_punkte[1:]

    print()  # Abstand zwischen den Arbeiten (im Terminal)
