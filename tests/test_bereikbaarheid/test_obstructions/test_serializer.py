import datetime

import pytest
from marshmallow import ValidationError

from bereikbaarheid.obstructions.serializer import ObstructionsSerializer


class TestObstructionSerializer:
    def test_time_to_GTE_time_from_validate(self):
        ObstructionsSerializer().load(
            {
                "timeFrom": "00:00",
                "timeTo": "12:00",
                "date": "2023-01-01",
            }
        )

    def test_time_to_GTE_time_from_validate_ERROR(self):
        with pytest.raises(ValidationError):
            ObstructionsSerializer().load(
                {
                    "timeFrom": "23:00",
                    "timeTo": "15:00",
                    "date": "2023-01-01",
                }
            )

    def test_post_load_variables(self):
        """
        Verify that the post_load on the serializer is added the
        datetime_from and datetime_to variables
        :return:
        """
        data = ObstructionsSerializer().load(
            {
                "timeFrom": "00:00",
                "timeTo": "12:00",
                "date": "2023-01-01",
            }
        )
        assert "datetime_from" in data
        assert "datetime_to" in data
        assert "time_from" in data
        assert "time_to" in data
        assert "date" in data
        assert isinstance(data["datetime_from"], datetime.datetime)
        assert isinstance(data["datetime_to"], datetime.datetime)
