from api.api_manager import ApiManager
import pytest


class TestMovieAPI:
    @pytest.mark.parametrize("min_price,max_price,location,genre_id",
    [
        (1, 1000, "msk", 1),
        (10, 500, "spb", 2)
    ])
    @pytest.mark.slow
    def test_get_all_movies(self, api_manager: ApiManager,
                            min_price,
                            max_price,
                            location,
                            genre_id):
        """
        Тест на получение всех фильмов
        """
        payload = {"minPrice": min_price,
                   "maxPrice": max_price,
                   "location": location,
                   "genreId": genre_id
                   }
        response = api_manager.movie_api.get_all_movies(params=payload, expected_status=200)
        response_data = response.json()


        assert response_data["pageSize"] == 10, "Pagination size is not 10"
