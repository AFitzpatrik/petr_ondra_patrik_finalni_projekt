import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Event, Country, City, Comment, Type, Location
from viewer.utils import format_country_name, format_city_name


class CountryModelForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = "__all__"
        labels = {"name": "Název země: "}
        help_texts = {"name": "Zadej oficiální anglický název státu"}

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        print(f"CountryModelForm clean_name called with: '{name}'")

        # Povolujeme české znaky, čísla a běžné znaky
        if not re.fullmatch(r"[A-Za-zÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž0-9\-\.\(\) ]+", name):
            print(f"Validation failed for: '{name}'")
            raise ValidationError("Název smí obsahovat pouze písmena, čísla, mezery a běžné znaky (-.()).")

        formatted_name = format_country_name(name)
        print(f"Formatted name: '{formatted_name}'")

        if Country.objects.filter(name__iexact=formatted_name).exists():
            print(f"Country already exists: '{formatted_name}'")
            raise ValidationError("Země s tímto názvem již existuje.")

        print(f"Returning formatted name: '{formatted_name}'")
        return formatted_name


class CityModelForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["name", "country", "zip_code"]
        labels = {"name": "Město: ", "country": "Země: ", "zip_code": "PSČ: "}
        help_texts = {
            "name": "Zadej jméno města",
            "country": "Vyber stát kde se město nachází",
            "zip_code": "Zadej PSČ města",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-select"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        print(f"CityModelForm clean_name called with: '{name}'")
        
        # Povolujeme české znaky, čísla a běžné znaky
        if not re.fullmatch(r"[A-Za-zÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž0-9\-\.\(\) ]+", name):
            raise ValidationError("Název smí obsahovat pouze písmena, čísla, mezery a běžné znaky (-.()).")
        
        formatted_name = format_city_name(name)
        print(f"Formatted city name: '{formatted_name}'")
        return formatted_name

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get("zip_code", "").replace(" ", "").strip()
        print(f"CityModelForm clean_zip_code called with: '{zip_code}'")
        if not re.fullmatch(r"\d{4,5}", zip_code):
            print(f"Zip code validation failed for: '{zip_code}'")
            raise ValidationError(
                "PSČ musí obsahovat 4 nebo 5 čísel bez mezer a pomlček."
            )
        print(f"Zip code validation passed for: '{zip_code}'")
        return zip_code

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name", "").strip()
        country = cleaned_data.get("country")
        zip_code = cleaned_data.get("zip_code", "").replace(" ", "").strip()

        if name and country and zip_code:
            exists = (
                City.objects.filter(
                    name__iexact=name, country=country, zip_code__iexact=zip_code
                )
                .exclude(pk=self.instance.pk)
                .exists()
            )

            if exists:
                raise ValidationError(
                    "Město s tímhle názvem a PSČ již v tomto státě existuje."
                )

        return cleaned_data


class TypeModelForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ["name"]
        labels = {"name": "Název typu"}

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        
        # Povolujeme české znaky, čísla a běžné znaky
        if not re.fullmatch(r"[A-Za-zÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž0-9\-\.\(\) ]+", name):
            raise ValidationError("Název smí obsahovat pouze písmena, čísla, mezery a běžné znaky (-.()).")
        
        if Type.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Type with this Name already exists.")
        return name


class LocationModelForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "address", "city"]
        labels = {"name": "Název místa", "address": "Adresa", "city": "Město"}

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        
        # Povolujeme české znaky, čísla a běžné znaky
        if not re.fullmatch(r"[A-Za-zÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž0-9\-\.\(\) ]+", name):
            raise ValidationError("Název smí obsahovat pouze písmena, čísla, mezery a běžné znaky (-.()).")
        
        return name

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name", "").strip()
        address = cleaned_data.get("address", "").strip()
        city = cleaned_data.get("city")

        if name and address and city:
            exists = (
                Location.objects.filter(
                    name__iexact=name, address__iexact=address, city=city
                )
                .exclude(pk=self.instance.pk)
                .exists()
            )

            if exists:
                raise ValidationError(
                    "Location with this Name and Address already exists."
                )
        return cleaned_data


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "type",
            "description",
            "start_date_time",
            "end_date_time",
            "event_image",
            "location",
            "capacity",
        ]
        widgets = {
            "start_date_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "end_date_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }
        labels = {
            "capacity": "Počet míst",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["start_date_time", "end_date_time"]:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime(
                    "%Y-%m-%dT%H:%M"
                )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date_time")
        end = cleaned_data.get("end_date_time")
        if start and end and end < start:
            self.add_error(None, "Konec události nemůže být dříve než začátek.")
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Napište komentář..."}
            ),
        }
        labels = {
            "content": "",
        }
