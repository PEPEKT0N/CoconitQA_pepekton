import time


from model.page_objects_models import WitcherInfo

def test_review_movie(autorized_page, review_movie):
    witcher_page = WitcherInfo(autorized_page)
    witcher_page.open()
    witcher_page.set_rating(review_movie)
    witcher_page.assert_allert_was_pop_up()
    witcher_page.make_screenshot_and_attach_to_allure()

    time.sleep(5)