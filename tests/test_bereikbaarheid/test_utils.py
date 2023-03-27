import pytest

from bereikbaarheid.utils import convert_to_bool, django_query_db


class TestUtils:
    @pytest.mark.django_db
    def test_django_query_db(self):
        query = "select 1"
        result = django_query_db(query, {})
        assert result == [(1,)]

    @pytest.mark.parametrize(
        "value, expected_value",
        [
            ("true", True),
            ("false", False),
            (1, True),
            (0, False),
            ("gibberish", False)
        ],
    )
    def test_convert_to_bool(self, value, expected_value):
        assert expected_value == convert_to_bool(value)
