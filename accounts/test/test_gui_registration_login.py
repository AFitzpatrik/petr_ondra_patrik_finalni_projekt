import pytest
from playwright.async_api import async_playwright
from .test_data_generator import TestDataGenerator


class TestUserRegistration:
    @pytest.mark.asyncio
    async def test_user_registration_and_login(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            try:
                user_data = TestDataGenerator.generate_user_data()

                print(f"\n=== TEST REGISTRACE ===")
                for key, value in user_data.items():
                        print(f"{key.capitalize()}: {value}")
                print(f"========================")

                #Test registrace
                await self._test_registration(page, user_data)

                #Test přihlášení
                await self._test_login(page, user_data)

            except Exception as e:
                print(f"Chyba v testu: {e}")
                print(f"Aktuální URL: {page.url}")
                raise

            finally:
                await browser.close()

    async def _test_registration(self, page, user_data):
        await page.goto("http://127.0.0.1:8000/accounts/signup/")
        await page.wait_for_load_state('networkidle')

        #Vyplnění formuláře
        await page.fill("#id_first_name", user_data['first_name'])
        await page.fill("#id_last_name", user_data['last_name'])
        await page.fill("#id_username", user_data['username'])
        await page.fill("#id_password1", user_data['password'])
        await page.fill("#id_password2", user_data['password'])
        await page.fill("#id_email", user_data['email'])
        await page.fill("#id_date_of_birth", user_data['date_of_birth'])
        await page.fill("#id_phone", user_data['phone'])

        #Odeslání formuláře
        await page.click('text="Registrovat se"')

        #Ověření úspěšné registrace
        await page.wait_for_url("**/accounts/registration_success/", timeout=10000)
        await page.wait_for_timeout(4000)

        #Asserty pro ověření url
        assert "registration_success" in page.url
        success_message = await page.locator("h1, h2, .success").first.text_content()
        assert success_message is not None, "Nenalezena zpráva o úspěšné registraci"

        print("✅ Registrace uživatele byla úspěšná!")

    async def _test_login(self, page, user_data):
        await page.click('text="Přihlásit se"')
        await page.wait_for_url("**/accounts/login/", timeout=10000)

        await page.fill("#id_username", user_data['username'])
        await page.fill("#id_password", user_data['password'])
        await page.click('text="Přihlásit se"')

        #Ověření úspěšného přihlášení
        await page.wait_for_url("**/accounts/login_success/", timeout=10000)
        await page.wait_for_timeout(4000)

        #Asserty pro login url
        assert "login_success" in page.url
        success_message = await page.locator("h1, h2, .success").first.text_content()
        assert success_message is not None, "Nenalezena zpráva o úspěšném přihlášení"

        print("✅ Přihlášení bylo úspěšné!")
