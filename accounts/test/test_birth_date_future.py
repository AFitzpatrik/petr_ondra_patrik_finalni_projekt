from datetime import timedelta, date
import pytest
from playwright.async_api import async_playwright
from .test_data_generator import TestDataGenerator

class TestBirthDateFuture:
    @pytest.mark.asyncio
    async def test_birth_date_is_in_future(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            try:
                user_data = TestDataGenerator.generate_user_data()
                future_date = (date.today() + timedelta(days=1)).isoformat()
                user_data['date_of_birth'] = future_date

                print(f"\n=== TEST DATUM NAROZENÍ V BUDOUCNOSTI ===")
                print(f"Datum narození: {future_date}")
                print(f"=============================================")

                await page.goto("http://127.0.0.1:8000/accounts/signup/")
                await page.wait_for_load_state('networkidle')

                await page.fill("#id_first_name", user_data['first_name'])
                await page.fill("#id_last_name", user_data['last_name'])
                await page.fill("#id_username", user_data['username'])
                await page.fill("#id_password1", user_data['password'])
                await page.fill("#id_password2", user_data['password'])
                await page.fill("#id_email", user_data['email'])
                await page.fill("#id_date_of_birth", future_date)
                await page.fill("#id_phone", user_data['phone'])

                await page.click('text="Registrovat se"')
                await page.wait_for_timeout(2000)

                assert "/accounts/signup/" in page.url

                # Hledáme chybovou zprávu v .alert.alert-danger
                error_message = await page.locator(".alert.alert-danger").first.text_content()
                assert error_message is not None
                assert "datum narození" in error_message.lower() or "budoucnosti" in error_message.lower()

                print("✅ Test data narození v budoucnosti proběhl úspěšně!")

            except Exception as e:
                print(f"Chyba v testu: {e}")
                print(f"Aktuální URL: {page.url}")
                raise

            finally:
                await browser.close()