import pytest
from marshmallow import ValidationError

from bereikbaarheid.validation import allowed_vehicle_types


class TestValidation:

    @pytest.mark.parametrize(
        'vehicle_type',
        [
            ('Bedrijfsauto'),
            ('Bus'),
            ('Personenauto'),
        ]
    )
    def test_allowed_vehicle_types(self, vehicle_type):
        """
        Not Raising an expection is passing
        :param vehicle_type:
        :param expected_result:
        :return:
        """
        allowed_vehicle_types(vehicle_type)

    def test_incorrect_allowed_vehicle_types(self):
        """
        Raise an exception if an incorrect value is passed
        :return:
        """

        with pytest.raises(ValidationError) as excinfo:
            allowed_vehicle_types('A Fake Value')

        assert "Moet één zijn van:" in str(excinfo.value)


