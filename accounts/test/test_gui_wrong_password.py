
import pytest
from playwright.async_api import async_playwright
from .test_data_generator import TestDataGenerator

class TestUserRegistrationWrongPassword:
    @pytest.mark.asyncio
    async def test_registration_with_mismatched_passwords(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            user_data = TestDataGenerator.generate_user_data()
            wrong_password = TestDataGenerator.random_password()
            while wrong_password == user_data['password']:
                wrong_password = TestDataGenerator.random_password()

            await page.goto("http://127.0.0.1:8000/accounts/signup/")
            await page.wait_for_load_state('networkidle')

            await page.fill("#id_first_name", user_data['first_name'])
            await page.fill("#id_last_name", user_data['last_name'])
            await page.fill("#id_username", user_data['username'])
            await page.fill("#id_password1", user_data['password'])
            await page.fill("#id_password2", wrong_password)
            await page.fill("#id_email", user_data['email'])
            await page.fill("#id_date_of_birth", user_data['date_of_birth'])
            await page.fill("#id_phone", user_data['phone'])

            await page.click('text="Registrovat se"')
            await page.wait_for_timeout(2000)

            assert "/accounts/signup/" in page.url

            #Hledám chybovou zprávu v .alert.alert-danger, jako máme v template
            error_message = await page.locator(".alert.alert-danger").first.text_content()
            assert error_message is not None
            assert "heslo" in error_message.lower()

            print("✅ Registrace s rozdílnými hesly správně selhala.")

            await browser.close()