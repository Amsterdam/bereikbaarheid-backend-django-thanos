import pytest

from bereikbaarheid.traffic_signs.query_conditions import (
    conditions,
    transform_categories,
)


class TestConditions:
    @pytest.mark.parametrize(
        "vehile_type, max_weight, trailer, expected_set",
        [
            ("BedrijfsAuto", 4500, True, {"C01", "C07", "C07ZB", "C07B", "C10"}),
            ("Bus", 4500, True, {"C01", "C07A", "C07B", "C10"}),
            ("BedrijfsAuto", 3000, False, {"C01"}),
            ("BedrijfsAuto", 3000, True, {"C01", "C10"}),
            ("Personenauto", 3000, True, {"C01", "C10"}),
        ],
    )
    def test_conditons(self, vehile_type, max_weight, trailer, expected_set):
        """
        Check if the send parameters produce the correct traffic_sign code conditions
        to filter one.
        :return:
        """
        result = conditions(vehile_type, max_weight, trailer)
        assert result == expected_set

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
