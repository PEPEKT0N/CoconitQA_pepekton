from custom_requester.custom_requester import CustomRequester
from constants.constants import MOVIES_URL, MOVIE_ENDPOINT, LOGIN_ENDPOINT


class MovieAPI(CustomRequester):
    """
    Класс для работы с API movies.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_URL)
        self.session = session

    def get_all_movies(self, endpoint=MOVIE_ENDPOINT, params=None, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=endpoint,
            params=params,
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        """
        Создание нового фильма (требуется авторизация).
        :param movie_data: Данные о фильме.
        :param expected_status: Ожидаемый статус-код.
        :return: Ответ с данными созданного фильма.
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIE_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def get_movie_info(self, movie_id, expected_status=200):
        """
        Получение информации о фильме.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """
        Удаление фильма.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def update_movie(self, movie_id, new_data, expected_status=200):
        """
        Частичное обновление данных о фильме
        :param movie_id: ID фильма
        :param new_data: Новые данные о фильме
        :param expected_status: ожидаемый статус-код
        """
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            data=new_data,
            expected_status=expected_status
        )

