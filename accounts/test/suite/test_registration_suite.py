import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from test_gui_registration_login import TestUserRegistration
from test_gui_wrong_password import TestUserRegistrationWrongPassword
from test_birth_date_future import TestBirthDateFuture

class TestRegistrationSuite:
    """Test suite - volá existující testy bez duplikace kódu"""

    @pytest.mark.asyncio
    async def test_suite_registration_and_login(self, page):
        """Test úspěšné registrace a přihlášení v suite"""
        test_instance = TestUserRegistration()
        await test_instance.test_user_registration_and_login_suite(page)

    @pytest.mark.asyncio
    async def test_suite_wrong_password(self, page):
        """Test neúspěšné registrace s rozdílnými hesly v suite"""
        test_instance = TestUserRegistrationWrongPassword()
        await test_instance.test_registration_with_mismatched_passwords_suite(page)

    @pytest.mark.asyncio
    async def test_suite_future_birth_date(self, page):
        """Test neúspěšné registrace s datem v budoucnosti v suite"""
        test_instance = TestBirthDateFuture()
        await test_instance.test_birth_date_is_in_future_suite(page) 