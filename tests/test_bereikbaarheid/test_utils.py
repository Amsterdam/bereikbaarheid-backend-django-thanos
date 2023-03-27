import pytest

from bereikbaarheid.utils import django_query_db


class TestUtils:
    @pytest.mark.django_db
    def test_django_query_db(self):
        query = "select 1"
        result = django_query_db(query, {})
        assert result == [(1,)]
