from playwright.sync_api import Page
import random
import allure

from model.page_objects_models import BasePage

class CinescopeMovieReviewer(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = None  

        self.login_button = "button[text()='Войти']"
        self.review_text_area = "textarea[name='text']"
        self.rate_button = "xpath=//button[@type='button' and @role='combobox']"
        self.submit_button = "button[type='submit']"
        self.details_button = "button[text='Подробнее']"

    @allure.step("Выбор первого фильма на главной странице")
    def select_first_movie(self):
        """
        Находит первый фильм на главной странице по кнопке 'Подробнее' и переходит на его страницу.
        """
        
        if self.page.url != self.home_url:
            self.open_url(self.home_url)

        with allure.step("Получаем список всех доступных фильмов на главной странице"):
            details_buttons = self.page.get_by_role("button", name="Подробнее").all()
        
        if len(details_buttons) == 0:
            raise AssertionError("Не найдено ни одного фильма на главной странице")          
        
        with allure.step(f"Нажимаем по первой кнопке 'Подробнее' (найдено фильмов: {len(details_buttons)})"):
            details_buttons[0].click()        
        
        with allure.step("Ожидаем перехода на страницу фильма"):
            self.page.wait_for_url(f"{self.home_url}movies/**", timeout=5000)
            self.url = self.page.url

    @allure.step("Открытие страницы фильма")
    def open(self):
        """
        Открывает страницу фильма, динамически выбирая первый доступный фильм на главной странице.
        """
        self.select_first_movie()

    @allure.step("Ввод текста отзыва: {text_rating}")
    def enter_review(self, text_rating: str):
        """
        Заполняет textarea отзывом о фильме
        """
        self.enter_text_to_element(self.review_text_area, text_rating)

    @allure.step("Установка рейтинга фильма")
    def set_rating(self):
        """
        Выставляет рандомный рейтинг от 1 до 5 включительно.
        random.randint(1, 5) возвращает случайное целое число от 1 до 5 включительно.
        """
        rate = str(random.randint(1, 5))
        self.click_element(self.rate_button)
        self.page.get_by_role("option", name=rate).click()

    @allure.step("Отправка отзыва с текстом: {text_rating}")
    def submit_review(self, text_rating: str):
        """
        Написание отзыва, выставление рейтинга и отправка данных
        """
        self.enter_review(text_rating)
        self.set_rating()
        self.click_element(self.submit_button)

    @allure.step("Проверка появления уведомления об успешном создании отзыва")
    def assert_alert_was_pop_up(self):
        self.check_pop_p_element_with_text("Отзыв успешно создан")