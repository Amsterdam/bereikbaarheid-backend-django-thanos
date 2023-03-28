from datetime import date, datetime, time
from unittest.mock import MagicMock, patch

import pytest

from bereikbaarheid.obstructions.obstructions import (
    _transform_results,
    get_obstructions,
)

QUERY_RESULT = [
    (
        {
            "type": "MultiLineString",
            "coordinates": [[4.866495892366908, 52.35413098888868]],
        },
        17970,
        "Koninginneweg",
        333,
        [
            {
                "activity": "Vernieuwing",
                "reference": "De Koninginneweg is volledig afgesloten voor doorgaand verkeer. We vernieuwen de Koninginneweg en het noordelijk deel van het Valeriusplein.",
                "url": "https://www.amsterdam.nl/projecten/werkzaamheden/overige/koninginneweg-afsluiting/",
                "start_date": "2022-05-30T00:00:00",
                "end_date": "2023-05-30T00:00:00",
            }
        ],
    )
]


class TestObstructions:
    @pytest.mark.parametrize(
        "query_results, expected_result",
        [
            (
                QUERY_RESULT,
                [
                    {
                        "type": "Feature",
                        "geometry": QUERY_RESULT[0][0],
                        "properties": {
                            "road_element_id": QUERY_RESULT[0][1],
                            "road_element_street_name": QUERY_RESULT[0][2],
                            "road_element_accessibility_code": QUERY_RESULT[0][3],
                            "obstructions": QUERY_RESULT[0][4],
                        },
                    }
                ],
            )
        ],
    )
    def test__transform_results(self, query_results, expected_result):
        result = _transform_results(query_results)
        assert result == expected_result

    @pytest.mark.django_db
    @patch(
        "bereikbaarheid.obstructions.obstructions.django_query_db",
        MagicMock(return_value=QUERY_RESULT),
    )
    def test_get_obstructions(self):
        """
        Mock the query result because of an empty db and check if the flow works
        with input parameters. Input parameters are not valid for the query result for
        this unit test because of the mock
        :return:
        """
        serialized_data = {
            "time_from": time(12, 0),
            "time_to": time(23, 0),
            "date": date(2023, 1, 1),
            "datetime_from": datetime(2023, 1, 1, 12, 0),
            "datetime_to": datetime(2023, 1, 1, 23, 0),
        }
        result = get_obstructions(serialized_data)
        assert len(result) == 1
