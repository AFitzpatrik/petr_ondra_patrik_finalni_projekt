import pytest
import random
import string
from playwright.async_api import async_playwright

def random_username(length=12): #Použití u username, name, lastname
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(characters, k=length))

def random_email(length=12):
    email = ''.join(random.choices(string.ascii_lowercase, k=length))
    return f"{email}@email.com"

def random_number(length=11):
    return ''.join(random.choices(string.digits, k=length))


@pytest.mark.asyncio  #Boilerplate, standartní nastavení playwright testu
async def test_user_registration_and_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) #NUTNO NAINSTALOVAT CHROMIUM (playwright install chromium)
        page = await browser.new_page()

        try:
            #Ošetření, že jedno stejné heslo pro obě pole
            password = random_password()
            username = random_username()
            email = random_email()
            first_name = random_username()
            last_name = random_username()
            phone = random_number()


            print(f"\n=== TEST REGISTRACE ===")
            print(f"Username: {username}")
            print(f"Jméno: {first_name}")
            print(f"Příjmení: {last_name}")
            print(f"Heslo: {password}")
            print(f"Email: {email}")
            print(f"Telefon: {phone}")
            print(f"========================")
        
            await page.goto("http://127.0.0.1:8000/accounts/signup/")
            
            #Čekání na načtení stránky
            await page.wait_for_load_state('networkidle')

            await page.fill("#id_first_name", first_name)
            await page.fill("#id_last_name", last_name)
            await page.fill("#id_username", username)
            await page.fill("#id_password1", password)
            await page.fill("#id_password2", password)
            await page.fill("#id_email", email)
            await page.fill("#id_date_of_birth", "1990-12-12")
            await page.fill("#id_phone", phone)

            #Odeslání formuláře skrz tlačíko
            await page.click('text="Registrovat se"')

            #Čekání na přesměrování na success stránku
            await page.wait_for_url("**/accounts/registration_success/")
            print("Registrace uživatele byla úspěšná!")
            await page.wait_for_timeout(5000)

            await page.click('text="Přihlásit se"')
            await page.wait_for_url("**/accounts/login/")

            await page.fill("#id_username", username)
            await page.fill("#id_password", password)
            await page.click('text="Přihlásit se"')
            await page.wait_for_url("**/accounts/login_success/")
            print("Přihlášení bylo úspěšné!")
            await page.wait_for_timeout(5000)




        except Exception as e:
            print(f"Chyba v testu: {e}")
            print(f"Aktuální URL: {page.url}")

        finally:
            await browser.close()
