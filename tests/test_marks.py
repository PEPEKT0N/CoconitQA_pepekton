import pytest


@pytest.fixture
def setup_data():
    print("Setup")

class TestMarks:
    @pytest.mark.skip(reason="Временно отключен")
    def test_example(self):
        assert 1 + 1 == 2

    skip_test = True

    @pytest.mark.skipif(skip_test, reason="Тест временно отключен вручную")
    def test_skipif_demo(self):
        assert True

    @pytest.mark.xfail(reason="Функция еще не реализована")
    def test_future_feature(self):
        assert 1 == 2



    @pytest.mark.usefixtures("setup_data")
    def test_with_usefixture(self):
        assert True