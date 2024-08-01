import glob
import os

from django.db.models import QuerySet
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect

from funktionen import get_uuid
from kontrollen.forms import KontrolleErstellen
from kontrollen.models import Kontrollen, Erstellt

from aufgaben.models import Themen

path = '/'.join(os.path.abspath(__file__).split('\\')[:-2])


def kontrollen(request):
    context_kontrollen: QuerySet = Kontrollen.objects.all().filter(sichtbar=True).order_by('identifier')
    if len(context_kontrollen) == 0:
        return render(request, 'noKontrollen.html')
    else:
        return render(request, 'kontrollen.html',
                      {'Kontrollen': context_kontrollen})


def view(request, identifier: str):
    identifier = identifier.replace('.pdf', '')
    beispiel = True if identifier.split(' ')[0] == 'Beispiel' else False
    if beispiel:
        name = Kontrollen.objects.filter(identifier=' '.join(identifier.split(' ')[1:])).get().name
        return render(request, 'viewKontrolle.html', {'beispiel': beispiel,
                                                      'name': f'Beispiel: {name}',
                                                      'identifier': identifier,
                                                      'path': f'{path}/skripteKontrollen/pdf/{name}'})
    else:
        try:
            name = Kontrollen.objects.filter(identifier=' '.join(identifier.split(' ')[:-1])).get().name
            return render(request, 'viewKontrolle.html', {'beispiel': beispiel, 'name': name,
                                                          'identifier': identifier,
                                                          'path': f'{path}/skripteKontrollen/pdf/{name}'})
        except:
            name = identifier
            return render(request, 'viewKontrolle.html', {'beispiel': beispiel, 'name': name,
                                                          'identifier': identifier,
                                                          'path': f'{path}/skripteKontrollen/pdf/{name}'})


def pdf(response, identifier):
    file_path = f'{path}/skripteKontrollen/pdf/{identifier}.pdf'
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def beispiel(response, identifier):
    file_path = f'{path}/skripteKontrollen/pdf/beispiele/{identifier}.pdf'
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def download(response, identifier):
    file_path = f'{path}/skripteKontrollen/pdf/{identifier}.pdf'
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response


def erstellen(identifier, schule='', schulart='', kurs='', lehrer='', klasse='', titel='', datum='', probe=True, aufgaben=None, schnell=False):
    themenbereich = Themen.objects.filter(name=identifier).exists()
    uuid = get_uuid()
    cwd = os.getcwd()
    os.chdir(f'{path}/skripteKontrollen')
    if themenbereich:
        os.system(f'python "themen.py" "{identifier}" "{uuid}" "0:{schule}" "1:{schulart}" "2:{kurs}" '
                  f'"4:{klasse}" "5:{lehrer}" "7:{titel}" "8:{datum}" "{probe}" "{aufgaben}"')
    elif schnell:
        os.system(f'python "{identifier}.py" "{uuid}" "{probe}"')
    else:
        os.system(f'python "{identifier}.py" "{uuid}" "0:{schule}" "1:{schulart}" "2:{kurs}" '
                  f'"4:{klasse}" "5:{lehrer}" "8:{datum}" "{probe}"')
    os.chdir(cwd)
    kontrolle = Erstellt(identifier=identifier, uuid=uuid)
    kontrolle.save()
    return uuid


def probe_erstellen(request, identifier):
    uuid = erstellen(identifier, schnell=True)

    return redirect(to=f'/kontrollen/{identifier} {uuid}')


def kontrolle_erstellen(request, identifier, aufgaben=None):
    stufe = Themen.objects.get(name=identifier).stufe
    try:
        name = Kontrollen.objects.get(identifier=identifier)
    except:
        name = identifier

    if request.method == 'POST':
        form = KontrolleErstellen(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            schule = form.cleaned_data['schule']
            schulart = form.cleaned_data['schulart']
            kurs = form.cleaned_data['kurs']
            lehrer = form.cleaned_data['lehrer']
            klasse = form.cleaned_data['klasse']
            titel = form.cleaned_data['titel']
            titel = titel if titel is not '' else identifier
            datum = form.cleaned_data['datum'].strftime('%d.%m.%Y') if form.cleaned_data['datum'] is not None else None
            kontrollen_art = form.cleaned_data['kontrollen_art']
            probe = True if kontrollen_art == 'Probe' else False
            uuid = erstellen(identifier, schule, schulart, kurs, lehrer,
                             klasse, titel, datum, probe, aufgaben)

            return redirect(to=f'/kontrollen/{identifier} {uuid}')
    else:
        form = KontrolleErstellen()

    return render(request, 'erstellen.html', context={'form': form, 'identifier': identifier, 'name': name, 'stufe': stufe})
