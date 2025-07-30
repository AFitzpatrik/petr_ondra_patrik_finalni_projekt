from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import SignUpForm
from accounts.models import Profile


class SignUpFormTest(TestCase):
    
    def test_duplicate_email_validation(self):
        """Test, že se zobrazí chyba při duplicitním emailu"""
        # Vytvoření prvního uživatele
        user1 = User.objects.create_user(
            username="testuser1",
            email="test@example.com",
            password="testpass123"
        )
        
        # Vytvoření formuláře s duplicitním emailem
        form_data = {
            'username': 'testuser2',
            'email': 'test@example.com',  # Stejný email
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('Tento e-mail je již registrován.', str(form.errors['email']))
    
    def test_duplicate_phone_validation(self):
        """Test, že se zobrazí chyba při duplicitním telefonu"""
        # Vytvoření prvního uživatele s profilem
        user1 = User.objects.create_user(
            username="testuser1",
            email="user1@example.com",
            password="testpass123"
        )
        Profile.objects.create(user=user1, phone="123456789")
        
        # Vytvoření formuláře s duplicitním telefonem
        form_data = {
            'username': 'testuser2',
            'email': 'user2@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '123456789'  # Stejný telefon
        }
        
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertIn('Tento telefon je již registrován.', str(form.errors['phone']))
    
    def test_valid_registration(self):
        """Test, že validní registrace projde"""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '987654321'
        }
        
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
