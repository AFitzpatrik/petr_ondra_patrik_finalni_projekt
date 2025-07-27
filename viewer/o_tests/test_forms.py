from django.test import TestCase
from django.contrib.auth.models import User, Permission
from viewer.models import Type, City, Country, Location
from django.urls import reverse
from viewer.forms import EventForm
from django.utils import timezone
from datetime import timedelta


class ExtendedFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

        permission = Permission.objects.get(codename="add_event")
        self.user.user_permissions.add(permission)

        self.country = Country.objects.create(name="Česko")
        self.city = City.objects.create(
            name="Praha", country=self.country, zip_code="11000"
        )
        self.location = Location.objects.create(
            name="Výstaviště",
            description="Velká hala",
            address="U výstaviště 1",
            city=self.city,
        )
        self.event_type = Type.objects.create(name="Koncert")
        self.client = Client()

        self.test_image_path = os.path.join(
            os.path.dirname(__file__), "media", "test_image.jpg"
        )
        assert os.path.exists(self.test_image_path), "Test image not found!"

    def test_add_type_with_permission(self):
        response = self.client.post(reverse("type_create"), {"name": "Výstava"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Type.objects.filter(name="Výstava").exists())

    def test_add_type_with_duplicate_name(self):
        Type.objects.create(name="Výstava")
        response = self.client.post(reverse("type_create"), {"name": "Výstava"})
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFormError(form, "name", ["Type with this Name already exists."])

    def test_add_type_without_permission(self):
        self.client.logout()
        User.objects.create_user(username="bezprava", password="pass")
        self.client.login(username="bezprava", password="pass")

        response = self.client.post(reverse("type_create"), {"name": "Přednáška"})
        self.assertEqual(response.status_code, 403)

    def test_add_location_with_permission(self):
        data = {
            "name": "Sál B",
            "address": "Vedlejší 789",
            "city": self.city.id,
        }
        response = self.client.post(reverse("location_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Location.objects.filter(name="Sál B", address="Vedlejší 789").exists()
        )

    def test_add_location_with_duplicate_name(self):
        data = {
            "name": "Sál A",
            "address": "Hlavní 123",
            "city": self.city.id,
        }
        response = self.client.post(reverse("location_create"), data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        non_field_errors = form.non_field_errors()
        self.assertIn(
            "Location with this Name and Address already exists.", non_field_errors
        )

    def test_add_location_without_permission(self):
        self.client.logout()
        User.objects.create_user(username="bezpravalokace", password="pass")
        self.client.login(username="bezpravalokace", password="pass")

        data = {
            "name": "Bez práv",
            "address": "Někde 456",
            "city": self.city.id,
        }
        response = self.client.post(reverse("location_create"), data)
        self.assertEqual(response.status_code, 403)

    def test_event_form_end_before_start(self):
        start = timezone.now()
        end = start - timedelta(hours=1)
        form_data = {
            "name": "Test Událost",
            "type": Type.objects.create(name="Workshop").id,
            "description": "Test popis",
            "start_date_time": start.strftime("%Y-%m-%dT%H:%M"),
            "end_date_time": end.strftime("%Y-%m-%dT%H:%M"),
            "event_image": "",
            "location": self.location.id,
            "capacity": 10,
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Konec události nemůže být dříve než začátek.", form.non_field_errors()
        )
