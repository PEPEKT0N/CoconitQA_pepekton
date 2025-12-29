import pytest

@pytest.mark.parametrize("parameter_name", ["value1", "value2"])
class TestParametrizeClass:
    def test_first(self, parameter_name):
        print(f"Test 1 progon: {parameter_name}")
        assert True

    def test_second(self, parameter_name):
        print(f"Test 2 progon: {parameter_name}")
        assert True

