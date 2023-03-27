from unittest.mock import MagicMock, patch

import pytest

from bereikbaarheid.isochrones.isochrones import _transform_results, get_isochrones

QUERY_RESULT = [
    (
        24379,
        1158098,
        {
            "type": "LineString",
            "coordinates": [
                [120912.8359375, 490748.21875],
                [120955.34375, 490802.09375],
            ],
        },
    )
]


class TestIsochrones:
    @pytest.mark.parametrize(
        "query_results, expected_result",
        [
            (
                QUERY_RESULT,
                [
                    {
                        "properties": {
                            "id": QUERY_RESULT[0][0],
                            "totalcost": QUERY_RESULT[0][1],
                        },
                        "geometry": QUERY_RESULT[0][2],
                        "type": "Feature",
                    }
                ],
            )
        ],
    )
    def test__transform_results(self, query_results, expected_result):
        result = _transform_results(query_results)
        assert result == expected_result

    @patch(
        "bereikbaarheid.isochrones.isochrones.django_query_db",
        MagicMock(return_value=QUERY_RESULT),
    )
    def test_get_traffic_signs(self):
        """
        Mock the query result because of an empty db and check if the flow works
        with input parameters. Input parameters are not valid for the query result for
        this unit test because of the mock
        :return:
        """
        serialized_data = {"lat": 52.363066102529295, "lon": 4.907205867943042}
        result = get_isochrones(serialized_data)
        assert len(result) == 1
