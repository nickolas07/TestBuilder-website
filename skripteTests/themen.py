def run(path: str, identifier: str, uuid: str, titel: str, schule: str, schulart: str, kurs: str, klasse: int, lehrer: str,
        datum: str, probe: bool, aufgaben: str):

    import importlib
    import sys
    import string

    sys.path.append(f'{path}/skripteTests')
    from skripte.erstellen import seite, test_erzeugen
    from funktionen import get_aufgaben

    import django

    django.setup()
    from aufgaben.models import Themen

    temp_aufgaben = aufgaben[1:-1].split(', ')
    aufgaben = {}
    for aufgabe in temp_aufgaben:
        aufgabe = aufgabe.replace('"', '')
        try:
            aufgaben[aufgabe.split(': ')[0]] = int(aufgabe.split(': ')[1])
        except ValueError:
            aufgaben[aufgabe.split(': ')[0]] = aufgabe.split(': ')[1]


    art = 'Probe' if probe else 'Test'
    if titel is None:
        titel = identifier
    fach = Themen.objects.get(name=identifier).fach

    # Aufgaben
    temp_alle_aufgaben = get_aufgaben(identifier)
    aufgaben_name = []
    for a, aufgabe in enumerate(temp_alle_aufgaben, start=1):
        aufgaben_name.append([f'Aufgabe_{a}', aufgabe[1], aufgabe[3][0]])


    alphabet = string.ascii_lowercase
    alle_aufgaben = []
    for a, aufgabe in enumerate(temp_alle_aufgaben, start=1):
        temp_aufgabe = [f'Aufg_{aufgabe[0]}']
        temp_teilaufgabe_list = []
        for teilaufgabe in aufgabe[-1]:
            temp_teilaufgabe = '_'.join(teilaufgabe[0].replace('.', '_').split('_')[1:])
            temp_teilaufgabe_list.append(f'Aufg_{a}_{temp_teilaufgabe}')
        temp_aufgabe.append(temp_teilaufgabe_list)
        temp_add = []
        for add in aufgabe[-2][0]:
            if add[0].isupper():
                temp_add.append(f'{add}_{a}')
            else:
                temp_add.append(f'{add.capitalize()}_{a}')
        temp_aufgabe.append(temp_add)
        temp_aufgabe.append(aufgabe[-2][0])
        alle_aufgaben.append(temp_aufgabe)

    brauch_aufg = []
    brauch_teilaufg = []
    brauch_params = []

    for key, value in aufgaben.items():
        if key.startswith('Aufgabe_') and key.count('_') == 1:
            brauch_aufg.append(key)
        elif key.startswith('Aufgabe_') and key.count('_') == 2:
            brauch_teilaufg.append(key)
        else:
            brauch_params.append(key)

    params_dict = {}
    for item in brauch_params:
        suffix = item.split('_')[-1]
        if suffix not in params_dict:
            params_dict[suffix] = []
        params_dict[suffix].append(item)

    brauch_params = params_dict

    # [name_funktion, [teilaufgaben], [parameter {name: value}, {name: value}]] | [name_funktion, [parameter {name: value}, {name: value}]]
    selected = []
    for aufgabe in brauch_aufg:
        aufgabe_nr = int(aufgabe.split('_')[1])

        # holt den namen der Funktion
        name_aufgabe = None
        for item in aufgaben_name:
            if item[0] == aufgabe:
                name_aufgabe = item[1]
                break

        # holt die Parameter
        parameter = {}
        for aufg, params in brauch_params.items():
            namen_params = alle_aufgaben[aufgabe_nr-1][3]
            for param in params:
                if param.endswith(str(aufgabe_nr)):
                    if namen_params[params.index(param)] == 'BE':
                        if isinstance(aufgaben[param], str):
                            parameter[namen_params[params.index(param)]] = list(map(lambda x: int(x), aufgaben[param].split('-')))
                        else:
                            parameter[namen_params[params.index(param)]] = [aufgaben[param]]
                    elif isinstance(aufgaben[param], str):
                        if aufgaben[param] == 'Ja':
                            parameter[namen_params[params.index(param)]] = True
                        elif aufgaben[param] == 'Nein':
                            parameter[namen_params[params.index(param)]] = False
                        else:
                            parameter[namen_params[params.index(param)]] = aufgaben[param].lower()
                    else:
                        parameter[namen_params[params.index(param)]] = aufgaben[param]

        # holt die Teilaufgaben
        alphabet = string.ascii_lowercase
        teilaufgaben = []
        for teilaufg in brauch_teilaufg:
            if teilaufg.split('_')[1] == str(aufgabe_nr):
                teilaufgaben.append(alphabet[int(teilaufg.split('_')[-1])-1])

        # fügt alles zusammen
        if name_aufgabe is not None:
            selected.append([name_aufgabe, teilaufgaben, parameter]) if len(teilaufgaben) != 0 else selected.append([name_aufgabe, parameter])

    liste_punkte = ['Punkte']
    liste_bez = ['Aufgabe']

    aufgaben_seite1 = []

    module = importlib.import_module(f'Aufgaben.{Themen.objects.get(name=identifier).stufe}_{identifier}')

    for i, aufgabe in enumerate(selected, start=1):
        func = getattr(module, aufgabe[0])
        if len(aufgabe) == 3:
            aufgaben_seite1.append(func(i, aufgabe[1], **aufgabe[2]))
        elif len(aufgabe) == 2:
            aufgaben_seite1.append(func(i, **aufgabe[1]))

    for element in aufgaben_seite1:
        liste_bez.extend(element[5])
        liste_punkte.extend(element[4])

    liste_seiten = [seite(aufgaben_seite1)]

    angaben = [schule, schulart, kurs, fach, klasse, lehrer, art, titel, datum, liste_bez, liste_punkte, False,
               identifier, uuid]

    test_erzeugen(liste_seiten, angaben, probe=probe)
