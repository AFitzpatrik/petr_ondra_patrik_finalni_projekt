import random
import string
import pytest
from playwright.async_api import async_playwright

class TestDataGenerator:#Generování testovacích dat

    @staticmethod
    def random_username(length=7):
        return 'TEST-' + ''.join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def random_password(length=12):
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(characters, k=length))

    @staticmethod
    def random_email(length=12):
        email = ''.join(random.choices(string.ascii_lowercase, k=length))
        return f"{email}@email.com"

    @staticmethod
    def random_phone(length=11):
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    def generate_user_data():

        return {
            'username': TestDataGenerator.random_username(),
            'first_name': TestDataGenerator.random_username(),
            'last_name': TestDataGenerator.random_username(),
            'password': TestDataGenerator.random_password(),
            'email': TestDataGenerator.random_email(),
            'phone': TestDataGenerator.random_phone(),
            'date_of_birth': '1990-12-12'
        }