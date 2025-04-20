# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_data import ApiData  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.kidbright_data import KidbrightData  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_controller_get_api_condition_count(self):
        """Test case for controller_get_api_condition_count

        Get count of each condition for API data
        """
        response = self.client.open(
            '/laundry-api/v1/api/conditioncount',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_api_data_avg(self):
        """Test case for controller_get_api_data_avg

        Get average values of API data
        """
        response = self.client.open(
            '/laundry-api/v1/api/avg',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_api_data_by_id(self):
        """Test case for controller_get_api_data_by_id

        Get API data by ID
        """
        response = self.client.open(
            '/laundry-api/v1/api/{data_id}'.format(data_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_api_data_by_timerange(self):
        """Test case for controller_get_api_data_by_timerange

        Get API data within a specific time range
        """
        query_string = [('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/laundry-api/v1/api/timerange',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_api_data_latest(self):
        """Test case for controller_get_api_data_latest

        Get the latest API data
        """
        response = self.client.open(
            '/laundry-api/v1/api/latest',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_api_data_recent_days(self):
        """Test case for controller_get_api_data_recent_days

        Get average data for the last N days
        """
        query_string = [('days', 7)]
        response = self.client.open(
            '/laundry-api/v1/api/recentdays',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_api_hourly_avg(self):
        """Test case for controller_get_api_hourly_avg

        Retrieve hourly average data for temperature, wind speed, and humidity
        """
        response = self.client.open(
            '/laundry-api/v1/api/hourly-avg',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_kidbright_avg(self):
        """Test case for controller_get_kidbright_avg

        Get average values of KidBright data
        """
        response = self.client.open(
            '/laundry-api/v1/kidbright/avg',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_kidbright_by_id(self):
        """Test case for controller_get_kidbright_by_id

        Get KidBright data by ID
        """
        response = self.client.open(
            '/laundry-api/v1/kidbright/{data_id}'.format(data_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_kidbright_by_timerange(self):
        """Test case for controller_get_kidbright_by_timerange

        Get KidBright data within a specific time range
        """
        query_string = [('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/laundry-api/v1/kidbright/timerange',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_kidbright_data(self):
        """Test case for controller_get_kidbright_data

        Get the last 50 KidBright data entries
        """
        response = self.client.open(
            '/laundry-api/v1/kidbright',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_kidbright_hourly_average(self):
        """Test case for controller_get_kidbright_hourly_average

        Get hourly average values for KidBright data
        """
        response = self.client.open(
            '/laundry-api/v1/kidbright/hourlyavg',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_kidbright_min_max(self):
        """Test case for controller_get_kidbright_min_max

        Get min and max values for KidBright data
        """
        response = self.client.open(
            '/laundry-api/v1/kidbright/minmax',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_latest_kidbright_data(self):
        """Test case for controller_get_latest_kidbright_data

        Get the latest KidBright data
        """
        response = self.client.open(
            '/laundry-api/v1/kidbright/latest',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
