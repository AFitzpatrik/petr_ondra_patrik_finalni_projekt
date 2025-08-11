import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

@pytest_asyncio.fixture(scope="session")
async def browser():
    #Jeden browser pro všechny testy pro suite
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()

@pytest_asyncio.fixture
async def page(browser):
    #Nová page pro každý test
    page = await browser.new_page()
    yield page
    await page.close() 