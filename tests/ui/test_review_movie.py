import pytest
import allure

from model.cinescope_movie_reviewer import CinescopeMovieReviewer

@allure.epic("UI тестирование")
@allure.feature("Функционал отзывов")
@allure.story("Оставление отзыва на фильм")
@allure.description("""
Тест проверяет функционал оставления отзыва на первый фильм  с главной страницы.
Шаги:
1. Авторизация пользователя
2. Выбор первого доступного фильма на главной странице
3. Заполнение текста отзыва
4. Выбор рейтинга (случайное значение от 1 до 5)
5. Отправка отзыва
6. Проверка появления уведомления об успешном создании отзыва
""")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Тест оставления отзыва на фильм")
@pytest.mark.ui
@pytest.mark.slow
def test_review_movie(authorized_page, review_movie):
    movie_page = CinescopeMovieReviewer(authorized_page)
    movie_page.open()
    movie_page.submit_review(review_movie)
    movie_page.assert_alert_was_pop_up()
    movie_page.make_screenshot_and_attach_to_allure()