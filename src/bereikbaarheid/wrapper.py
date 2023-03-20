import json
import urllib

from django.http import HttpRequest, JsonResponse
from marshmallow import ValidationError


def _extract_parameters(request: HttpRequest) -> dict:
    """
    Extract the parameters from either a get or post request
    and transform them to a dict
    :param request:
    :return:
    """
    if request.META["REQUEST_METHOD"] == "GET":
        return dict(urllib.parse.parse_qsl(request.META["QUERY_STRING"]))
    else:
        return json.loads(request.body)


def validate_data(serializer):
    """
    Validate the incoming data through the selected serializer and validate the input.
    On valid it will pass through the validate data
    On invalid it will return a 400 Http with the error message
    :param serializer:
    :return:
    """

    def decorator(func):
        def wrapper(view, request, *args, **kwargs):
            try:
                data = serializer().load(_extract_parameters(request))
                kwargs["serialized_data"] = data
                return func(view, request, *args, **kwargs)
            except ValidationError as err:
                return JsonResponse(status=400, data=err.messages)
            except json.JSONDecodeError as e:
                return JsonResponse(status=400, data={"error": str(e)})

        return wrapper

    return decorator


def geo_json_response(func):
    """
    Wrap any dict into a geojson format and return it as a json response
    :param func:
    :return:
    """

    def wrapped(*args, **kwargs):
        return JsonResponse(
            status=200,
            data={"feature": func(*args, **kwargs), "type": "FeatureCollection"},
        )

    return wrapped
