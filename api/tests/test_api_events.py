from datetime import timedelta
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APITestCase

from viewer.models import Event, Country, City, Location, Type


class APIEventsTest(APITestCase):
    def setUp(self):
        print('-' * 80)
        print(f"Spouští se test: {self._testMethodName}")

        self.user = User.objects.create_user(username='Nunu', password='test123')

        country = Country.objects.create(name='Česká republika')
        city = City.objects.create(name='Plzeň', country=country)
        self.location = Location.objects.create(name='Hala lokomotivy', city=city)
        self.event_type = Type.objects.create(name='Koncert')

        self.now_time = now()

        self.future = Event.objects.create(
            name='Koncert zítra',
            start_date_time=self.now_time + timedelta(days=1),
            end_date_time=self.now_time + timedelta(days=1, hours=2),
            description='Koncert, který se bude konat.',
            owner_of_event=self.user,
            location=self.location,
            type=self.event_type
        )

        self.active = Event.objects.create(
            name='Probíhající koncert',
            start_date_time=self.now_time - timedelta(hours=2),
            end_date_time=self.now_time + timedelta(hours=4),
            description='Koncert probíhající dvě hodiny a bude ještě čtyři hodiny trvat.',
            owner_of_event=self.user,
            location=self.location,
            type=self.event_type
        )

        self.past = Event.objects.create(
            name='Včerejší koncert',
            start_date_time=self.now_time - timedelta(days=1, hours=2),
            end_date_time=self.now_time - timedelta(days=1),
            description='Koncert, který proběhl včera',
            owner_of_event=self.user,
            location=self.location,
            type=self.event_type
        )

    def test_api_events_requires_authentication(self):
        response = self.client.get(reverse('api_events'))
        self.assertEqual(response.status_code, 401)

    def test_api_all_events_requires_authentication(self):
        response = self.client.get(reverse('all_events'))
        self.assertEqual(response.status_code, 401)

    def test_api_filtered_events_requires_authentication(self):
        url = reverse('filtered_events') + '?start=2025-01-01T00:00:00&end=2025-12-31T23:59:59'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_events_returns_future_events(self):
        self.client.login(username='Nunu', password='test123')
        response = self.client.get(reverse('api_events'))
        self.assertEqual(response.status_code, 200)

        names = [event['name'] for event in response.data]

        self.assertIn(self.future.name, names)
        self.assertNotIn(self.active.name, names)
        self.assertNotIn(self.past.name, names)

    def test_api_events_returns_all_events(self):
        self.client.login(username='Nunu', password='test123')
        response = self.client.get(reverse('all_events'))
        self.assertEqual(response.status_code, 200)

        names = [event['name'] for event in response.data]

        self.assertIn(self.future.name, names)
        self.assertIn(self.active.name, names)
        self.assertIn(self.past.name, names)

    def test_api_events_returns_filtered_events(self):
        self.client.login(username='Nunu', password='test123')
        start = (self.now_time - timedelta(hours=3)).isoformat(timespec='seconds')
        end = (self.now_time + timedelta(days=2)).isoformat(timespec='seconds')

        params = urlencode({'start': start, 'end': end})
        url = reverse('filtered_events') + '?' + params

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        names = [event['name'] for event in response.data]

        self.assertIn(self.active.name, names)
        self.assertIn(self.future.name, names)
        self.assertNotIn(self.past.name, names)

    def test_api_filtered_events_empty_result(self):
        self.client.login(username='Nunu', password='test123')

        start = (self.now_time + timedelta(days=365)).isoformat(timespec='seconds')
        end = (self.now_time + timedelta(days=400)).isoformat(timespec='seconds')
        params = urlencode({'start': start, 'end': end})
        url = reverse('filtered_events') + '?' + params

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_api_filtered_events_missing(self):
        self.client.login(username='Nunu', password='test123')
        response = self.client.get(reverse('filtered_events'))
        self.assertEqual(response.status_code, 200)

    def test_api_filtered_events_invalid_params(self):
        self.client.login(username='Nunu', password='test123')
        url = reverse('filtered_events') + '?start=blbost&end=blbost'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
