from datetime import datetime, time

import pytz
from marshmallow import Schema, ValidationError, fields, post_load, validates_schema

tz_amsterdam = pytz.timezone("Europe/Amsterdam")


class ObstructionsSerializer(Schema):
    date = fields.Date(
        format="%Y-%m-%d",
        load_default=lambda: datetime.today().astimezone(tz_amsterdam),
        required=False,
    )

    time_from = fields.Time(
        format="%H:%M", load_default=time.min, required=False, data_key="timeFrom"
    )

    time_to = fields.Time(
        format="%H:%M", load_default=time.max, required=False, data_key="timeTo"
    )

    @post_load
    def merge_date_time(self, data: dict, **kwargs):
        """
        merge the date and time fields to create extra datetime fields
        :param data:
        :param kwargs:
        :return:
        """
        data["datetime_from"] = datetime.combine(data["date"], data["time_from"])
        data["datetime_to"] = datetime.combine(data["date"], data["time_to"])

        return data

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if data["time_to"] < data["time_from"]:
            raise ValidationError("TimeTo must be later than timeFrom")
