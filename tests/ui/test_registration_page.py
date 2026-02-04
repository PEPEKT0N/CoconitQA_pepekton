import time
from playwright.sync_api import sync_playwright

from model.page_objects_models import CinescopeRegisterPage
from utils.data_generator import DataGenerator

def test_register_by_ui():
    with sync_playwright() as playwright:
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_full_name()
        random_password = DataGenerator.generate_random_password()

        browser = playwright.chromium.launch(headless=False)
        page =browser.new_page()

        register_page = CinescopeRegisterPage(page)

        register_page.open()
        register_page.register(random_name, random_email, random_password, random_password)

        register_page.assert_was_redirect_to_login_page()

        register_page.assert_allert_was_pop_up()

        time.sleep(5)

        browser.close()