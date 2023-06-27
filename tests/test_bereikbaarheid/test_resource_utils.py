import datetime

import pytest

from bereikbaarheid.resources.utils import convert_str, convert_to_date, convert_to_time


class TestUtils:

    @pytest.mark.parametrize("test_input, expected", 
                             [("16/03/22 0:00", datetime.datetime(2022, 3, 16, 0, 0)), 
                              ("2022-02-11 00:00:00.000", datetime.datetime(2022, 2, 11, 0, 0)),
                              ("22-03-17", ValueError),
                              ("test", ValueError)])
    def test_convert_to_date(self, test_input, expected):
        """Raise an exception if value can't be converted to datetime format"""

        assert convert_to_date(test_input) == expected

    @pytest.mark.parametrize("test_input, expected", 
                             [("12:00", datetime.time(12, 0)), 
                              ("13:00:59", datetime.time(13, 0, 59)),
                              ("1", datetime.time(1, 0)),
                              ("test", ValueError)])
    def test_convert_to_time(self, test_input, expected):
        """Raise an exception if string can't be converted to needed time format"""

        assert convert_to_time(test_input) == expected

    @pytest.mark.parametrize("test_input, test_to, expected", 
                             [("1200", "float", 1200), 
                              ("1", "float", float(1)),
                              ("test", "float", "test"),
                              ("4", "set", "4")])
    def test_convert_str(self, test_input, test_to, expected):
        """Return to:format(value) else return value"""

        assert convert_str(test_input, test_to) == expected

