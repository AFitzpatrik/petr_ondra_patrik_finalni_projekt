from django.test import TestCase
from django.urls import reverse
from viewer.models import Country, City

class CitiesListViewTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='Česko')
        self.city = City.objects.create(name='Ostrava', country=self.country, zip_code='70030')

    def test_city_list_view_status_code(self):
        response = self.client.get(reverse('cities'))
        self.assertEqual(response.status_code, 200)

    def test_city_in_context(self):
        response = self.client.get(reverse('cities'))
        self.assertContains(response, 'Ostrava')

    def test_city_list_uses_correct_template(self):
        response = self.client.get(reverse('cities'))
        self.assertTemplateUsed(response, 'cities.html')