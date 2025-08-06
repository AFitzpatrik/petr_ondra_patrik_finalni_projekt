from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationTest(TestCase):

    def setUp(self):
        print(f"Spouští se test: {self._testMethodName}")

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="existujici", password="testheslo", email="existujici@email.cz"
        )

    def test_registration_success(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "novyuzivatel",
                "password1": "testheslo123",
                "password2": "testheslo123",
                "email": "novy@uzivatel.cz",
            },
        )
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(User.objects.filter(username="novyuzivatel").exists())

    def test_registration_password_mismatch(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "uzivatel2",
                "password1": "heslo1",
                "password2": "heslo2",
                "email": "uzivatel2@uzivatel.cz",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hesla se neshodují.")

    def test_registration_duplicate_username(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "existujici",
                "password1": "testheslo123",
                "password2": "testheslo123",
                "email": "duplicitni@email.cz",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Uživatel s tímto jménem již existuje.")

    def test_registration_invalid_email(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "uzivatel3",
                "password1": "testheslo123",
                "password2": "testheslo123",
                "email": "neplatnyemail",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vložte platnou e-mailovou adresu.")

    def test_registration_missing_required_field(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "",
                "password1": "testheslo123",
                "password2": "testheslo123",
                "email": "uzivatel4@uzivatel.cz",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toto pole je vyžadováno.")
