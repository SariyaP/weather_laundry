# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response20010 import InlineResponse20010  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from swagger_server.models.inline_response2008 import InlineResponse2008  # noqa: E501
from swagger_server.test import BaseTestCase


class TestForecastController(BaseTestCase):
    """ForecastController integration test stubs"""

    def test_controller_forecast_humidity(self):
        """Test case for controller_forecast_humidity

        Forecast humidity for the next 14 days
        """
        response = self.client.open(
            '/laundry-api/v1/forecast/humidity',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_forecast_light(self):
        """Test case for controller_forecast_light

        Forecast light for the next 14 days
        """
        response = self.client.open(
            '/laundry-api/v1/forecast/light',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_forecast_temperature(self):
        """Test case for controller_forecast_temperature

        Forecast temperature for the next 14 days
        """
        response = self.client.open(
            '/laundry-api/v1/forecast/temperature',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_predict_w_condition_next14_days(self):
        """Test case for controller_predict_w_condition_next14_days

        Forecast weather conditions for the next 14 days
        """
        response = self.client.open(
            '/laundry-api/v1/forecast-weather-conditions',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
