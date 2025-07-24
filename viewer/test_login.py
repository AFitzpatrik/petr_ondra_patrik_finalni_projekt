from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginTest(TestCase):

    def setUp(self):
        print(f'Spouští se test: {self._testMethodName}')

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='logintest', password='passwordtest')


    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'logintest',
            'password': 'passwordtest',
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('home'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_wrong_input(self):
        response = self.client.post(reverse('login'), {
            'username': 'logintest',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zadejte správnou hodnotu pole uživatelské jméno a heslo.")