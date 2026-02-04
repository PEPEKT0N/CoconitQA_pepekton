import time
from playwright.sync_api import sync_playwright

from model.page_objects_models import CinescopeLoginPage

def test_login_by_ui(registered_user):
    with sync_playwright() as playwright:
        user_data, _ = registered_user
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        login_page = CinescopeLoginPage(page)

        login_page.open()
        login_page.login(user_data.email, user_data.password)

        login_page.assert_was_redirect_to_home_page()
        login_page.make_screenshot_and_attach_to_allure()
        login_page.assert_allert_was_pop_up()

        time.sleep(5)

        browser.close()