from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.db.utils import IntegrityError

from viewer.models import Event, Country, City, Location, Type


class EventModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(name="Česká republika")
        city = City.objects.create(name="Plzeň", country=country, zip_code=33333)

        location = Location.objects.create(
            name="Hala lokomotivy",
            description="Sportovní hala Lokomotiva Plzeň",
            address="Úslavská 2357",
            city=city
        )
        event_type = Type.objects.create(name="Sportovní")
        user = User.objects.create_user(username="testuser", password="testpassword")

        start_time = now()
        end_time = start_time + timedelta(hours=2)

        event = Event.objects.create(
            name="Judo mistrovství ČR",
            type=event_type,
            description="Mistrovství ČR v judu kategorie U18",
            start_date_time=start_time,
            end_date_time=end_time,
            owner_of_event = user,
            location = location
        )

    def setUp(self):
        print("-" * 80)


    def test_country_str(self):
        country = Country.objects.get(id=1)
        print(f"test_country_str: {country.__str__()}")
        self.assertEqual(str(country), "Česká republika")

    def test_country_unique_constraint(self):
        print(f"test_country_unique_constraint: trying to insert duplicate 'Česká republika'")
        with self.assertRaises(IntegrityError):
            Country.objects.create(name="Česká republika")

    def test_city_str(self):
        city =City.objects.get(id=1)
        print(f"test_city_str: {city.__str__()}")
        self.assertEqual(str(city), "Plzeň")

    def test_city_country_relationship(self):
        city = City.objects.get(id=1)
        print(f"test_city_country_relationship: '{city.name}' is in '{city.country.name}'")
        self.assertEqual(city.country.name, "Česká republika")

    def test_location_repr(self):
        location = Location .objects.get(id=1)
        expected = f"Location(name=Hala lokomotivy, city=Plzeň, address=Úslavská 2357)"
        print(f"test_location_repr: {repr(location)}")
        self.assertEqual(repr(location), expected)

    def test_location_city_relationship(self):
        location = Location.objects.get(id=1)
        print(f"test_location_city_relationship: '{location.name}' is in '{location.city.name}'")
        self.assertEqual(location.city.name, "Plzeň")

    def test_type_str(self):
        type = Type.objects.get(id=1)
        print(f"test_type_str: {type.__str__()}")
        self.assertEqual(str(type), "Sportovní")

    def test_type_unique_constraint(self):
        print(f"test_type_unique_constraint: trying to insert duplicate 'Sportovní'")
        with self.assertRaises(IntegrityError):
            Type.objects.create(name="Sportovní")

    def test_event_str(self):
        event = Event.objects.get(id=1)
        print(f"test_event_str: {event.__str__()}")
        expected = f"Judo mistrovství ČR ({event.start_date_time.strftime('%d.%m.%Y')})"
        self.assertEqual(str(event), expected)

    def test_event_type_relationship(self):
        event = Event.objects.get(id=1)
        print(f"test_event_type_relationship: '{event.type.name}' is in '{event.type.name}'")
        self.assertEqual(event.type.name, "Sportovní")

    def test_event_get_start_date_cz_format(self):
        event = Event.objects.get(id=1)
        expected = event.start_date_time.strftime('%d.%m.%Y, %H:%M')
        print(f"test_event_get_start_date_cz_format: {event.get_start_date_cz_format()}")
        self.assertEqual(event.get_start_date_cz_format(), expected)

    def test_event_get_end_date_cz_format(self):
        event = Event.objects.get(id=1)
        expected = event.end_date_time.strftime('%d.%m.%Y, %H:%M')
        print(f"test_event_get_start_date_cz_format: {event.get_end_date_cz_format()}")
        self.assertEqual(event.get_end_date_cz_format(), expected)




















