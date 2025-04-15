import connexion
import six

from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from swagger_server.models.inline_response2008 import InlineResponse2008  # noqa: E501
from swagger_server import util


def controller_forecast_humidity():  # noqa: E501
    """Forecast humidity for the next 14 days

     # noqa: E501


    :rtype: List[InlineResponse2007]
    """
    return 'do some magic!'


def controller_forecast_light():  # noqa: E501
    """Forecast light for the next 14 days

     # noqa: E501


    :rtype: List[InlineResponse2008]
    """
    return 'do some magic!'


def controller_forecast_temperature():  # noqa: E501
    """Forecast temperature for the next 14 days

     # noqa: E501


    :rtype: List[InlineResponse2006]
    """
    return 'do some magic!'
