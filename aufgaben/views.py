import json

from django.shortcuts import render, redirect

from funktionen import get_aufgaben
from aufgaben.models import Themen


def view_aufgaben(request, themenbereich):
    stufe = Themen.objects.get(name=themenbereich).stufe
    temp = get_aufgaben(themenbereich)
    aufgaben = []
    params = []
    for aufgabe in temp:
        temp_params = []
        aufgaben.append(aufgabe[2:])
        split_params = str(aufgabe[-2][1]).split(' ')
        for param in split_params:
            if param != 'None':
                if param.split('=')[1].startswith('['):
                    temp_list = param.split('=')[1][1:-1].split(',')
                    param = [param.split('=')[0], 'selection', temp_list]
            else:
                param = None
            if type(param) == list or param is None:
                temp_params.append(param)
            else:
                temp_params.append(param.split('='))

        params.append(temp_params)

    if request.method == 'POST':
        form_data = request.POST.dict()
        del form_data['csrfmiddlewaretoken']
        temp_form_data = form_data.copy()

        for key, value in temp_form_data.items():
            if value == '' or value == 'Keine Vorschrift':
                form_data.pop(key)

        aufgaben = []
        for key in form_data.keys():
            if key.startswith('Aufgabe'):
                aufgaben.append(key.lstrip('Aufgabe'))

        temp_form_data = form_data.copy()
        for key in temp_form_data.keys():
            temp = []
            for aufgabe in aufgaben:
                if key.endswith(aufgabe):
                    temp.append(True)
                else:
                    temp.append(False)
            if not any(temp):
                form_data.pop(key)

        return_data = {}
        for key, value in form_data.items():
            temp_key = key.split(' ')
            return_key = '_'.join(temp_key)
            if key.startswith('BE'):
                return_value = '-'.join(value.replace(' ', '').split(','))
            else:
                temp_value = value.split(' ')
                try:
                    temp_value = int(temp_value[0])
                except ValueError:
                    pass
                if isinstance(temp_value, int):
                    return_value = temp_value
                else:
                    temp_value = str(temp_value[0])
                    if not temp_value[-1].split('_')[1:]:
                        return_value = temp_value
                    else:
                        return_value = '_'.join([temp_value, '_'.join(temp_value[-1].split('_')[1:])])

            return_data[return_key] = return_value

        json_data = json.dumps(return_data)
        print('JSON output', json_data)

        return redirect(to=f'/tests/erstellen/{themenbereich}/{json_data}')

    return render(request, 'aufgaben.html', {'aufgaben': aufgaben, 'themenbereich': themenbereich, 'stufe': stufe, 'parameter': params})
