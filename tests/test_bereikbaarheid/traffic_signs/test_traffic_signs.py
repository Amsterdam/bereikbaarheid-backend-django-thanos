import pytest

from unittest.mock import patch, MagicMock

from bereikbaarheid.traffic_signs.traffic_signs import raw_query, get_traffic_signs, \
    _transform_results
from bereikbaarheid.utils import django_query_db


QUERY_RESULT = [(123, '1234', 'label_value', 'label',
                'oost', 777, 'some_info', 555, 'category',
                'https://a_url.com', '{"geom":[4.12, 52.9]}',
                'weesperstraat')]


class TestTrafficSign:

    @pytest.mark.django_db
    def test_raw_query(self):
        """
        Only test the query to see if the structure and parameters are working.
        No data is returning because of empty database
        :return:
        """

        result = django_query_db(raw_query, {
            'verkeersborden_categorieen': [],
            'verkeersborden_codes': [],
            'lengte': 2,
            'breedte': 2,
            'hoogte': 6.02,
            'aslast_gewicht': 3899,
            'totaal_gewicht': 3899,
            'max_massa':  4899
        })
        assert result == []

    @pytest.mark.parametrize('query_results, expected_result',
                             [
                                 (QUERY_RESULT,
                                  [{
                                      'type': 'Feature',
                                      'properties': {
                                          'id': 123,
                                          'type': '1234',
                                          'label': 'label',
                                          'label_as_value': 'label_value',
                                          'additional_info': 'some_info',
                                          'category': 'category',
                                          'link_to_panoramic_image': 'https://a_url.com',
                                          'network_link_id': 777,
                                          'street_name': 'weesperstraat',
                                          'traffic_decree_id': 555,
                                          'view_direction_in_degrees':'oost'
                                      },
                                      'geometry': {'geom': [4.12, 52.9]}
                                  }]
                                  )
                             ])
    def test__transform_results(self, query_results, expected_result):

        result = _transform_results(query_results)
        assert result == expected_result

    @patch("bereikbaarheid.traffic_signs.traffic_signs.django_query_db",
           MagicMock(return_value=QUERY_RESULT))
    def test_get_traffic_signs(self):
        """
        Mock the query result because of an empty db and check if the flow works
        with input parameters. Input parameters are not valid for the query result for
        this unit test because of the mock
        :return:
        """
        serialized_data = {
            "total_gewicht": 100,
            "lengte": 5,
            "hoogte": 2,
            "aslast_gewicht": 20,
            "verkeersborden_categorieen": ["prohibition"],
            "aanhanger": False,
            "breedte": 2,
            "voertuig_type": 'Bedrijfsauto',
            "max_massa": 200
        }
        result = get_traffic_signs(serialized_data)
        assert len(result) == 1