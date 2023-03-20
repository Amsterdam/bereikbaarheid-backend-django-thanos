from unittest.mock import MagicMock, patch

import pytest

from bereikbaarheid.prohibitory.prohibitory import (_transform_results,
                                                    get_prohibitory)

QUERY_RESULT = [(123, 456, '{"geom":[4.12, 52.9]}')]


class TestProhibitory:
    @pytest.mark.parametrize(
        "query_results, expected_result",
        [
            (
                QUERY_RESULT,
                [
                    {
                        "type": "Feature",
                        "properties": {"bereikbaar_status_code": 456, "id": 123},
                        "geometry": {"geom": [4.12, 52.9]},
                    }
                ],
            )
        ],
    )
    def test__transform_results(self, query_results, expected_result):
        result = _transform_results(query_results)
        assert result == expected_result

    @patch(
        "bereikbaarheid.prohibitory.prohibitory.django_query_db",
        MagicMock(return_value=QUERY_RESULT),
    )
    def test_get_prohibitory(self):
        """
        Mock the query result because of an empty db and check if the flow works
        with input parameters. Input parameters are not valid for the query result for
        this unit test because of the mock
        :return:
        """
        serialized_data = {
            "permit_environmental_zone": False,
            "permit_7_5": False,
            "axle_weight": 3175,
            "has_trailer": False,
            "height": 3,
            "length": 6.2,
            "total_weight": 4899,
            "vehicle_type": "Bedrijfsauto",
            "width": 2.05,
            "max_weight": 4899,
            "company_car": True,
            "bus": False,
        }
        result = get_prohibitory(serialized_data)
        assert len(result) == 1
