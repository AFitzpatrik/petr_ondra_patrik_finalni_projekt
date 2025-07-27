import os
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from viewer.models import Event, Type, Location, City, Country


class EventCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Vytvoření uživatele + přidání oprávnění
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

        # Cesta k testovacímu obrázku
        self.test_image_path = os.path.join(
            os.path.dirname(__file__), "media", "test_image.jpg"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("event_create"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, f"/accounts/login/?next={reverse('event_create')}"
        )

    def test_logged_in_user_can_create_event(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("event_create"),
            {
                "name": "Test Událost",
                "type": self.event_type.id,
                "description": "Popis události",
                "start_date_time": "2025-07-15T18:00",
                "end_date_time": "2025-07-15T20:00",
                "location": self.location.id,
                "capacity": 100,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.name, "Test Událost")
        self.assertEqual(event.owner_of_event, self.user)

    def test_event_creation_saves_correct_data(self):
        self.client.login(username="testuser", password="password")
        with open(self.test_image_path, "rb") as img:
            form_data = {
                "name": "Test Událost",
                "type": self.event_type.id,
                "description": "Popis testovací události",
                "start_date_time": "2025-07-15T10:00",
                "end_date_time": "2025-07-15T12:00",
                "location": self.location.id,
                "event_image": img,
                "capacity": 50,
            }
            response = self.client.post(reverse("event_create"), form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(name="Test Událost").exists())

        event = Event.objects.get(name="Test Událost")
        self.assertEqual(event.description, "Popis testovací události")
        self.assertEqual(event.owner_of_event, self.user)

    def test_event_image_is_resized(self):
        self.client.login(username="testuser", password="password")
        with open(self.test_image_path, "rb") as img:
            form_data = {
                "name": "Událost s obrázkem",
                "type": self.event_type.id,
                "description": "Obrázek bude zmenšen",
                "start_date_time": "2025-07-20T14:00",
                "end_date_time": "2025-07-20T16:00",
                "location": self.location.id,
                "event_image": img,
                "capacity": 75,
            }
            response = self.client.post(reverse("event_create"), form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(name="Událost s obrázkem").exists())

        event = Event.objects.get(name="Událost s obrázkem")
        image_path = event.event_image.path
        with Image.open(image_path) as im:
            width, height = im.size
            self.assertLessEqual(width, 1200)
            self.assertLessEqual(height, 800)
