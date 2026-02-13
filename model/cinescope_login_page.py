from playwright.sync_api import Page

from model.page_objects_models import BasePage

class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"

        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"

        self.login_button = "button[type='submit']"
        self.register_button = "a[href='/register' and text()='Зарегистрироваться']"

        self.witcher_movie = "button[text='Подробнее']"

    def open(self):
        self.open_url(self.url)

    def login(self, email: str, password: str):
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.email_input, email)
        self.click_element(self.login_button)

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    def assert_alert_was_pop_up(self):
        self.check_pop_p_element_with_text("Вы вошли в аккаунт")