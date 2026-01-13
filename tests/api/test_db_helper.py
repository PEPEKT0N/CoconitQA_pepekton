import pytest

class TestDBHelper:
    def test_db_requests(self, super_admin, db_helper, created_test_user):
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email(created_test_user.email)

    def test_create_movie_in_DB(self, super_admin, db_helper, created_test_movie):
        assert created_test_movie == db_helper.get_movie_by_name(created_test_movie.name)