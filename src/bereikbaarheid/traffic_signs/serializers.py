from marshmallow import Schema, fields, validate, validates
from bereikbaarheid.validation import voertuig, allowed_vehicle_types


class TrafficSignsSerializer(Schema):
    verkeersborden_categorieen = fields.List(
        fields.String(
            required=True,
            validate=validate.OneOf(
                [
                    "prohibition",
                    "prohibition with exception",
                    "prohibition ahead",
                ]
            ),
        ),
        required=True,
        data_key='trafficSignCategories',
        validate=validate.Length(min=1)
    )

    aslast_gewicht = fields.Integer(
        required=True,
        data_key='vehicleAxleWeight',
        validate=[
            validate.Range(
                min=voertuig["aslast_gewicht"]["min"],
                max=voertuig["aslast_gewicht"]["max"],
            )
        ]
    )

    aanhanger = fields.Boolean(required=True, data_key='vehicleHasTrailer')

    hoogte = fields.Float(
        required=True,
        data_key='vehicleHeight',
        validate=[
            validate.Range(
                min=voertuig["hoogte"]["min"],
                max=voertuig["hoogte"]["max"],
                min_inclusive=False,
            )
        ]
    )

    lengte = fields.Float(
        required=True,
        data_key='vehicleLength',
        validate=[
            validate.Range(
                min=voertuig["lengte"]["min"], max=voertuig["lengte"]["max"]
            )
        ]
    )

    max_massa = fields.Integer(
        required=True,
        data_key='vehicleMaxAllowedWeight',
        validate=[
            validate.Range(
                min=voertuig["maximale_toegestaande_gewicht"]["min"],
                max=voertuig["maximale_toegestaande_gewicht"]["max"],
            )
        ]
    )

    totaal_gewicht = fields.Integer(
        required=True,
        data_key='vehicleTotalWeight',
        validate=[
            validate.Range(
                min=voertuig["totaal_gewicht"]["min"],
                max=voertuig["totaal_gewicht"]["max"],
            )
        ],
    )

    voertuig_type = fields.String(required=True, data_key='vehicleType')

    breedte = fields.Float(
        required=True,
        data_key='vehicleWidth',
        validate=[
            validate.Range(
                min=voertuig["breedte"]["min"], max=voertuig["breedte"]["max"]
            )
        ],
    )

    @validates("voertuig_type")
    def allowed_vehicle_types(self, value):
        allowed_vehicle_types(value)
