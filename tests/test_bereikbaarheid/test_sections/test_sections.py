from unittest.mock import MagicMock, patch

import pytest

from bereikbaarheid.sections.sections import (_transform_results, get_sections,
                                              raw_query)
from bereikbaarheid.utils import django_query_db

QUERY_RESULT = [
    (
        {
            "type": "MultiLineString",
            "coordinates": [
                [
                    [4.824582988284092, 52.39014691501629],
                    [4.824627745093572, 52.3901471276253],
                ]
            ],
        },
        10537,
        "Rhôneweg",
        [
            {
                "road_section_id": 10537,
                "direction": "oost",
                "additional_info": "verbod stil te staan",
                "days": '{" vr",za,zo}',
                "start_time": "00:00:00",
                "end_time": "06:00:00",
            }
        ],
    )
]


class TestSections:
    @pytest.mark.django_db
    def test_raw_query(self):
        """
        Only test the query to see if the structure and parameters are working.
        No data is returning because of empty database
        :return:
        """

        result = django_query_db(raw_query, {})
        assert result == []

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
                            "id": QUERY_RESULT[0][1],
                            "street_name": QUERY_RESULT[0][2],
                            "load_unload": QUERY_RESULT[0][3],
                        },
                    }
                ],
            )
        ],
    )
    def test__transform_results(self, query_results, expected_result):
        result = _transform_results(query_results)
        assert result == expected_result

    @patch(
        "bereikbaarheid.sections.sections.django_query_db",
        MagicMock(return_value=QUERY_RESULT),
    )
    def test_get_sections(self):
        """
        Mock the query result because of an empty db and check if the flow works
        with input parameters. Input parameters are not valid for the query result for
        this unit test because of the mock
        :return:
        """

        result = get_sections()
        assert len(result) == 1
