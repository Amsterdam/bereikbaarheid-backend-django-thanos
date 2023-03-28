from unittest.mock import MagicMock, patch

import pytest

from bereikbaarheid.permits.permits import _transform_results, get_permits

QUERY_RESULT = (
    1234,
    False,
    False,
    False,
    True,
    {"type": "Point", "coordinates": [4.906954526489455, 52.362918128638206]},
    23.12354,
    None,
    True,
)


class TestPermits:
    @pytest.mark.parametrize(
        "query_results, expected_result",
        [
            (
                QUERY_RESULT,
                {
                    "id": 1234,
                    "attributes": {
                        "heavy_goods_vehicle_zone": False,
                        "in_amsterdam": True,
                        "low_emission_zone": False,
                        "rvv_permit_needed": False,
                        "time_window": None,
                        "wide_road": True,
                        "distance_to_destination_in_m": 23.12354,
                        "geom": {
                            "type": "Point",
                            "coordinates": [4.906954526489455, 52.362918128638206],
                        },
                    },
                },
            )
        ],
    )
    def test__transforms_results(self, query_results, expected_result):
        result = _transform_results(query_results)
        assert result == expected_result

    @patch(
        "bereikbaarheid.permits.permits.django_query_db",
        MagicMock(return_value=QUERY_RESULT),
    )
    def test_get_permits(self):
        """
        Mock the query result because of an empty db and check if the flow works
        with input parameters. Input parameters are not valid for the query result for
        this unit test because of the mock
        :return:
        """
        serialized_data = {
            "total_weight": 100,
            "length": 5,
            "height": 2,
            "axle_weight": 20,
            "traffic_sign_categories": ["prohibition"],
            "trailer": False,
            "width": 2,
            "vehicle_type": "Bedrijfsauto",
            "max_weight": 200,
        }
        result = get_permits(serialized_data)
        assert "id" in result
        assert "attributes" in result
