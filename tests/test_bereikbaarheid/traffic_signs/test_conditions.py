import pytest

from bereikbaarheid.traffic_signs.query_conditions import transform_categories


class TestConditions:
    @pytest.mark.parametrize(
        "categories, expected_result",
        [
            (["prohibition"], ["verbod"]),
            (
                ["prohibition", "prohibition with exception"],
                ["verbod", "verbod, met uitzondering"],
            ),
            (["prohibition ahead"], ["vooraankondiging verbod"]),
            (
                ["prohibition", "prohibition with exception", "prohibition ahead"],
                ["verbod", "verbod, met uitzondering", "vooraankondiging verbod"],
            ),
        ],
    )
    def test_transform_categories(self, categories, expected_result):
        result = transform_categories(categories)

        assert result == expected_result
