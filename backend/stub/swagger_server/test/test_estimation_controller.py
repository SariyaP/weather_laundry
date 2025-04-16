# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response2009 import InlineResponse2009  # noqa: E501
from swagger_server.test import BaseTestCase


class TestEstimationController(BaseTestCase):
    """EstimationController integration test stubs"""

    def test_controller_estimate_drying_time(self):
        """Test case for controller_estimate_drying_time

        Estimate drying time based on temperature, humidity, and wind.
        """
        query_string = [('temp', 1.2),
                        ('humid', 1.2),
                        ('wind_kph', 1.2),
                        ('width', 2)]
        response = self.client.open(
            '/laundry-api/v1/estimate-drying-time',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
