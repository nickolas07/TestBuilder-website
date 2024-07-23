import glob
import os
import time

from django.db.models import QuerySet
from django.shortcuts import render, redirect

from kontrollen.models import Erstellt
from suchen.forms import Suchen

path = '/'.join(os.path.abspath(__file__).split('\\')[:-2])


# Create your views here.
def suchen(request):
    if request.method == 'POST':
        form = Suchen(request.POST)
        if form.is_valid():
            uuid = ''
            for value in form.cleaned_data.values():
                uuid += str(value).upper()
                uuid += '-' if len(uuid) == 4 else ''

            kontrolle_db: QuerySet = Erstellt.objects.filter(uuid=uuid).values()
            if kontrolle_db:
                kontrolle__db_str = f'{kontrolle_db[0]['identifier']} {kontrolle_db[0]['uuid']}'
            else:
                kontrolle__db_str = None

            kontrolle_file = glob.glob(f'{path}/skripteKontrollen/pdf/*{uuid}.pdf')
            kontrolle_file_str = kontrolle_file[0].split('\\')[1][:-4] if kontrolle_file else None

            if kontrolle__db_str == kontrolle_file_str and (
                    kontrolle__db_str is not None and kontrolle__db_str is not None):
                return redirect(to=f'/kontrollen/{kontrolle__db_str}/')
            else:
                return redirect(to=f'notFound/')
    else:
        form = Suchen()
    return render(request, 'suchen.html', {'form': form})


def not_found(request):
    return render(request, 'nichtGefunden.html')


def delete(request, name):
    Erstellt.objects.filter(uuid=name.split(' ')[-1]).delete()
    os.remove(f'{path}/skripteKontrollen/pdf/{name}.pdf')
    os.remove(f'{path}/skripteKontrollen/pdf/{name} - Lsg.pdf')
    time.sleep(1)
    return redirect(to=f'/')
