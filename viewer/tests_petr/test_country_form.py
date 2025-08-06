from django.test import TestCase
from viewer.forms import CountryModelForm
from viewer.models import Country


class CountryModelFormTest(TestCase):

    def setUp(self):
        print("-" * 80)
        print(f"Spouští se test: {self._testMethodName}")

    def test_valid_country_name_format(self):
        form_data = {'name': 'bosnia and herzegovina'}
        form = CountryModelForm(data=form_data)

        self.assertTrue(form.is_valid())
        country = form.save()
        self.assertEqual(country.name, 'Bosnia and Herzegovina')

    def test_duplicate_country_is_rejected(self):
        Country.objects.create(name='Czech Republic')

        form_data = {'name': '   czech  republic'}
        form = CountryModelForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("Země s tímto názvem již existuje", str(form.errors))

    def test_invalid_characters_are_rejected(self):
        form_data = {'name': 'Česká republika'}
        form = CountryModelForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("Název smí obsahovat pouze anglická", str(form.errors))


