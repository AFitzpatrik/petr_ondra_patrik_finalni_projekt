from django.test import TestCase
from django.contrib.auth.models import User, Permission
from viewer.models import Type, City, Country, Location
from django.urls import reverse


class ExtendedFormTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username="adminuser", password="pass")
        self.admin_user.user_permissions.add(
            Permission.objects.get(codename="add_type"),
            Permission.objects.get(codename="add_location")
        )
        self.client.login(username="adminuser", password="pass")

        self.country = Country.objects.create(name="Testland")
        self.city = City.objects.create(name="Test City", country=self.country)

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
        user = User.objects.create_user(username="bezprava", password="pass")
        self.client.login(username="bezprava", password="pass")

        response = self.client.post(reverse("type_create"), {"name": "Přednáška"})
        self.assertEqual(response.status_code, 403)

    def test_add_location_with_permission(self):
        data = {
            "name": "Sál A",
            "address": "Hlavní 123",
            "city": self.city.id,
        }
        response = self.client.post(reverse("location_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Location.objects.filter(name="Sál A", address="Hlavní 123").exists())

    def test_add_location_with_duplicate_name(self):
        Location.objects.create(name="Sál A", address="Hlavní 123", city=self.city)
        data = {
            "name": "Sál A",
            "address": "Hlavní 123",
            "city": self.city.id,
        }
        response = self.client.post(reverse("location_create"), data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        non_field_errors = form.non_field_errors()
        self.assertIn("Location with this Name and Address already exists.", non_field_errors)

    def test_add_location_without_permission(self):
        self.client.logout()
        user = User.objects.create_user(username="bezpravalokace", password="pass")
        self.client.login(username="bezpravalokace", password="pass")

        data = {
            "name": "Bez práv",
            "address": "Někde 456",
            "city": self.city.id,
        }
        response = self.client.post(reverse("location_create"), data)
        self.assertEqual(response.status_code, 403)
