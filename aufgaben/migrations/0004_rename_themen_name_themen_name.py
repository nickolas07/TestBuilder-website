# Generated by Django 5.1b1 on 2024-07-23 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aufgaben', '0003_themen_fach'),
    ]

    operations = [
        migrations.RenameField(
            model_name='themen',
            old_name='themen_name',
            new_name='name',
        ),
    ]
