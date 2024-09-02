from django.contrib import admin

from tests.models import Test, Erstellt


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(Erstellt)
class ErstellteTestsAdmin(admin.ModelAdmin):
    pass
