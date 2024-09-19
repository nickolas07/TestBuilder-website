from dateutil.utils import today
from django import forms


class TestErstellen(forms.Form):
    identifier = forms.CharField(label='identifier', widget=forms.HiddenInput(), required=False, localize=False)
    titel = forms.CharField(
        label='titel',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingTitel',
            'placeholder': 'Titel'
        }))
    schule = forms.CharField(
        label='schule',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingSchule',
            'placeholder': 'Schule'
        }))
    schulart = forms.CharField(
        label='schulart',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingSchulart',
            'placeholder': 'Schulart'
        }))
    kurs = forms.ChoiceField(
        label='kurs',
        required=False,
        choices=[
            ('Grundkurs', 'Grundkurs'),
            ('Leistungskurs', 'Leistungskurs'),
            ('G-Kurs', 'G-Kurs'),
            ('E-Kurs', 'E-Kurs')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'floatingKurs',
            'placeholder': 'Kurs'
        }))
    lehrer = forms.CharField(
        label='lehrer',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingLehrer',
            'placeholder': 'Lehrer'
        }))
    datum = forms.DateField(
        label='datum',
        required=False,
        initial=today,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'floatingDatum',
            'placeholder': 'Datum'
        }))
    test_art = forms.ChoiceField(
        label='test_art',
        required=False,
        choices=[
            ('Probe', 'Probe'),
            ('Test', 'Test')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'floatingArt',
            'aria-label': 'Test-Art'
        }))
    klasse = forms.IntegerField(
        label='klasse',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'floatingKlasse',
            'placeholder': 'Klasse'
        }))
