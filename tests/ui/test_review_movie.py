import time
from playwright.sync_api import sync_playwright

from model.page_objects_models import WitcherInfo, CinescopeLoginPage

def test_review_movie(login_data_user, review_movie):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        login_page = CinescopeLoginPage(page)
        login_page.open()
        login_page.login(login_data_user["email"], login_data_user["password"])
        login_page.assert_was_redirect_to_home_page()
        login_page.assert_allert_was_pop_up()

        witcher_page = WitcherInfo(page)
        witcher_page.open()
        witcher_page.set_rating(review_movie)
        witcher_page.assert_allert_was_pop_up()
        witcher_page.make_screenshot_and_attach_to_allure()

        #time.sleep(5)

        browser.close()