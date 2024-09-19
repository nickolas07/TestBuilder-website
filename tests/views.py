import glob
import os

from django.db.models import QuerySet
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect

from funktionen import get_uuid
from tests.forms import TestErstellen
from tests.models import Test, Erstellt

from aufgaben.models import Themen
from skripteTests import themen

path = '/'.join(os.path.abspath(__file__).split('\\')[:-2])


def tests(request):
    context_tests: QuerySet = Test.objects.all().filter(sichtbar=True).order_by('identifier')
    if len(context_tests) == 0:
        return render(request, 'keineTests.html')
    else:
        return render(request, 'tests.html',
                      {'Tests': context_tests})


def view(request, identifier: str):
    identifier = identifier.replace('.pdf', '')
    beispiel = True if identifier.split(' ')[0] == 'Beispiel' else False
    if beispiel:
        name = Test.objects.filter(identifier=' '.join(identifier.split(' ')[1:])).get().name
        return render(request, 'viewTest.html', {'beispiel': beispiel,
                                                      'name': f'Beispiel: {name}',
                                                      'identifier': identifier,
                                                      'path': f'{path}/skripteTests/pdf/{name}'})
    else:
        try:
            name = Test.objects.filter(identifier=' '.join(identifier.split(' ')[:-1])).get().name
            return render(request, 'viewTest.html', {'beispiel': beispiel, 'name': name,
                                                          'identifier': identifier,
                                                          'path': f'{path}/skripteTests/pdf/{name}'})
        except:
            name = identifier
            return render(request, 'viewTest.html', {'beispiel': beispiel, 'name': name,
                                                          'identifier': identifier,
                                                          'path': f'{path}/skripteTests/pdf/{name}'})


def pdf(response, identifier):
    file_path = f'{path}/skripteTests/pdf/{identifier}.pdf'
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def beispiel(response, identifier):
    file_path = f'{path}/skripteTests/pdf/beispiele/{identifier}.pdf'
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def download(response, identifier):
    file_path = f'{path}/skripteTests/pdf/{identifier}.pdf'
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response


def erstellen(identifier, schule='', schulart='', kurs='', lehrer='', klasse=0, titel=None, datum='', probe=True, aufgaben=None, schnell=False):
    themenbereich = Themen.objects.filter(name=identifier).exists()
    uuid = get_uuid()
    cwd = os.getcwd()
    os.chdir(f'{path}/skripteTests')
    if themenbereich:
        themen.run(path, identifier, uuid, titel, schule, schulart, kurs, klasse, lehrer, datum, probe, aufgaben)
    elif schnell:
        os.system(f'python "{identifier}.py" "{uuid}" "{probe}"')
    else:
        os.system(f'python "{identifier}.py" "{uuid}" "0:{schule}" "1:{schulart}" "2:{kurs}" '
                  f'"4:{klasse}" "5:{lehrer}" "8:{datum}" "{probe}"')
    os.chdir(cwd)
    test = Erstellt(identifier=identifier, uuid=uuid)
    test.save()
    return uuid


def probe_erstellen(request, identifier):
    uuid = erstellen(identifier, schnell=True)

    return redirect(to=f'/tests/{identifier} {uuid}')


def test_erstellen(request, identifier, aufgaben=None):
    stufe = Themen.objects.get(name=identifier).stufe
    try:
        name = Test.objects.get(identifier=identifier)
    except:
        name = identifier

    if request.method == 'POST':
        form = TestErstellen(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            schule = form.cleaned_data['schule']
            schulart = form.cleaned_data['schulart']
            kurs = form.cleaned_data['kurs']
            lehrer = form.cleaned_data['lehrer']
            klasse = form.cleaned_data['klasse']
            titel = form.cleaned_data['titel']
            titel = titel if titel != '' else identifier
            datum = form.cleaned_data['datum'].strftime('%d.%m.%Y') if form.cleaned_data['datum'] is not None else None
            test_art = form.cleaned_data['test_art']
            probe = True if test_art == 'Probe' else False
            uuid = erstellen(identifier, schule, schulart, kurs, lehrer,
                             klasse, titel, datum, probe, aufgaben)

            return redirect(to=f'/tests/{identifier} {uuid}')
    else:
        form = TestErstellen()

    return render(request, 'erstellen.html', context={'form': form, 'identifier': identifier, 'name': name, 'stufe': stufe})
