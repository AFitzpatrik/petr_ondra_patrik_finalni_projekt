from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now, timedelta

from viewer.models import Event, Location, City, Country, Type


class SearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='tester', password='12345')
        cls.country = Country.objects.create(name='Česká republika')
        cls.city=City.objects.create(name='Plzeň', country=cls.country)
        cls.location = Location.objects.create(name='Hala lokomotivy', city=cls.city)
        cls.event_type=Type.objects.create(name='Koncert')

        cls.future = Event.objects.create(
            name = 'Koncert zítra',
            start_date_time = now() + timedelta(days=1),
            end_date_time = now() + timedelta(days=1, hours=2),
            description='Koncert, který se bude konat.',
            owner_of_event=cls.user,
            location=cls.location,
            type = cls.event_type
        )

        cls.active = Event.objects.create(
            name = 'Probíhající koncert',
            start_date_time = now() - timedelta(hours=2),
            end_date_time = now() + timedelta(hours=4),
            description='Koncert probíhající dvě hodiny a bude ještě čtyři hodiny trvat.',
            owner_of_event=cls.user,
            location=cls.location,
            type = cls.event_type
        )

        cls.past = Event.objects.create(
            name = 'Včerejší koncert',
            start_date_time = now() - timedelta(days=1, hours=2),
            end_date_time = now() - timedelta(days=1),
            description='Koncert, který proběhl včera',
            owner_of_event=cls.user,
            location=cls.location,
            type = cls.event_type
        )

    def setUp(self):
        print('-' * 80)

    def test_search_by_name(self):
        response = self.client.get(reverse('search'), {'search':'zítra'})
        print("test_search_by_name")
        self.assertContains(response, 'Koncert zítra')
        self.assertNotContains(response, 'Probíhající koncert')
        self.assertNotContains(response, 'Včerejší koncert')

    def test_filter_future(self):
        response = self.client.get(reverse('search'), {'filter':'future'})
        print("test_filter_future:")
        self.assertContains(response, 'Koncert zítra')
        self.assertNotContains(response, 'Včerejší koncert')
        self.assertNotContains(response, 'Probíhající koncert')

    def test_filter_active_future(self):
        response = self.client.get(reverse('search'), {'filter':'active_future'})
        print("test_filter_active_future:")
        self.assertContains(response, 'Koncert zítra')
        self.assertContains(response, 'Probíhající koncert')
        self.assertNotContains(response, 'Včerejší koncert')

    def test_filter_all(self):
        response = self.client.get(reverse('search'), {'filter':'all'})
        print("test_filter_all:")
        self.assertContains(response, 'Koncert zítra')
        self.assertContains(response, 'Probíhající koncert')
        self.assertContains(response, 'Včerejší koncert')

    def test_empty_search_does_not_crash(self):
        print("test_empty_search_does_not_crash")
        response = self.client.get(reverse('search'), {'search': ''})
        self.assertEqual(response.status_code, 200)

    def test_search_is_case_insensitive(self):
        response = self.client.get(reverse('search'), {'search': 'KONCERT'})
        print("test_search_is_case_insensitive:")
        self.assertContains(response, 'Koncert zítra')
        self.assertContains(response, 'Probíhající koncert')
        self.assertContains(response, 'Včerejší koncert')

    def test_combined_search_active_future(self):
        response = self.client.get(reverse('search'),{
            'search':'koncert',
            'filter':'active_future'
        })
        print("test_combined_search_active_future:")
        self.assertContains(response, 'Probíhající koncert')
        self.assertContains(response, 'Koncert zítra')
        self.assertNotContains(response, 'Včerejší koncert')




