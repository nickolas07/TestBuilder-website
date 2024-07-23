from django.contrib import admin

from kontrollen.models import Kontrollen, Erstellt


@admin.register(Kontrollen)
class KontrollenAdmin(admin.ModelAdmin):
    pass


@admin.register(Erstellt)
class ErstellteKontrollenAdmin(admin.ModelAdmin):
    pass
