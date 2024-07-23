from django.db import models


# Create your models here.
class Themen(models.Model):
    name = models.CharField(max_length=100)
    stufe = models.CharField(choices=[('Mittelstufe', 'Mittelstufe'), ('Oberstufe', 'Oberstufe')], default='Oberstufe',
                             max_length=100)
    fach = models.CharField(max_length=100, default='Mathematik')

    def __str__(self):
        return self.name
