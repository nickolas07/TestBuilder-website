import glob
import os
import time

from django.db.models import QuerySet
from django.shortcuts import render, redirect

from tests.models import Erstellt
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

            test_db: QuerySet = Erstellt.objects.filter(uuid=uuid).values()
            if test_db:
                test_db_str = f'{test_db[0]['identifier']} {test_db[0]['uuid']}'
            else:
                test_db_str = None

            test_file = glob.glob(f'{path}/skripteTests/pdf/*{uuid}.pdf')
            test_file_str = test_file[0].split('\\')[1][:-4] if test_file else None

            if test_db_str == test_file_str and (
                    test_db_str is not None and test_db_str is not None):
                return redirect(to=f'/tests/{test_db_str}/')
            else:
                return redirect(to=f'nicht-gefunden/')
    else:
        form = Suchen()
    return render(request, 'suchen.html', {'form': form})


def not_found(request):
    return render(request, 'nichtGefunden.html')


def delete(request, name):
    Erstellt.objects.filter(uuid=name.split(' ')[-1]).delete()
    os.remove(f'{path}/skripteTests/pdf/{name}.pdf')
    os.remove(f'{path}/skripteTests/pdf/{name} - Lsg.pdf')
    time.sleep(1)
    return redirect(to=f'/')
