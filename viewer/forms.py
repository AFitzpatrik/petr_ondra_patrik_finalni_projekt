import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Event, Country, City
from django import forms
from .models import Comment


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']
        labels = {
            'name': 'Název státu',
        }
        help_texts = {
            'name': 'Zadej název státu'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'country', 'zip_code']
        labels = {
            'name': 'Město',
            'country': 'Stát',
            'zip_code': 'PSČ'
        }
        help_texts = {
            'name': 'Zadej jméno města',
            'country': 'Vyber stát kde se město nachází',
            'zip_code': 'Zadej PSČ města'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code', '').replace(' ', '').strip()
        if not re.fullmatch(r'\d{4,5}', zip_code):
            raise ValidationError('PSČ musí obsahovat 4 nebo pět čísel bez mezer a pomlček')
        return zip_code

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').strip()
        country = cleaned_data.get('country')
        zip_code = cleaned_data.get('zip_code', '').replace(' ', '').strip()

        if name and country and zip_code:
            exists = City.objects.filter(
                name__iexact=name,
                country=country,
                zip_code__iexact=zip_code
            ).exclude(pk=self.instance.pk).exists()

            if exists:
                raise ValidationError('Město s tímhle názvem a PSČ již v tomto státě existuje')

        return cleaned_data


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'type',
            'description',
            'start_date_time',
            'end_date_time',
            'event_image',
            'location',
        ]
        widgets = {
            'start_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Napište komentář...'}),
        }
        labels = {
            'content': '',
        }
