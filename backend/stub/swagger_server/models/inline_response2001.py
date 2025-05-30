# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class InlineResponse2001(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, min_temp: float=None, max_temp: float=None, min_light: float=None, max_light: float=None, min_humidity: float=None, max_humidity: float=None):  # noqa: E501
        """InlineResponse2001 - a model defined in Swagger

        :param min_temp: The min_temp of this InlineResponse2001.  # noqa: E501
        :type min_temp: float
        :param max_temp: The max_temp of this InlineResponse2001.  # noqa: E501
        :type max_temp: float
        :param min_light: The min_light of this InlineResponse2001.  # noqa: E501
        :type min_light: float
        :param max_light: The max_light of this InlineResponse2001.  # noqa: E501
        :type max_light: float
        :param min_humidity: The min_humidity of this InlineResponse2001.  # noqa: E501
        :type min_humidity: float
        :param max_humidity: The max_humidity of this InlineResponse2001.  # noqa: E501
        :type max_humidity: float
        """
        self.swagger_types = {
            'min_temp': float,
            'max_temp': float,
            'min_light': float,
            'max_light': float,
            'min_humidity': float,
            'max_humidity': float
        }

        self.attribute_map = {
            'min_temp': 'min_temp',
            'max_temp': 'max_temp',
            'min_light': 'min_light',
            'max_light': 'max_light',
            'min_humidity': 'min_humidity',
            'max_humidity': 'max_humidity'
        }
        self._min_temp = min_temp
        self._max_temp = max_temp
        self._min_light = min_light
        self._max_light = max_light
        self._min_humidity = min_humidity
        self._max_humidity = max_humidity

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2001':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_1 of this InlineResponse2001.  # noqa: E501
        :rtype: InlineResponse2001
        """
        return util.deserialize_model(dikt, cls)

    @property
    def min_temp(self) -> float:
        """Gets the min_temp of this InlineResponse2001.


        :return: The min_temp of this InlineResponse2001.
        :rtype: float
        """
        return self._min_temp

    @min_temp.setter
    def min_temp(self, min_temp: float):
        """Sets the min_temp of this InlineResponse2001.


        :param min_temp: The min_temp of this InlineResponse2001.
        :type min_temp: float
        """

        self._min_temp = min_temp

    @property
    def max_temp(self) -> float:
        """Gets the max_temp of this InlineResponse2001.


        :return: The max_temp of this InlineResponse2001.
        :rtype: float
        """
        return self._max_temp

    @max_temp.setter
    def max_temp(self, max_temp: float):
        """Sets the max_temp of this InlineResponse2001.


        :param max_temp: The max_temp of this InlineResponse2001.
        :type max_temp: float
        """

        self._max_temp = max_temp

    @property
    def min_light(self) -> float:
        """Gets the min_light of this InlineResponse2001.


        :return: The min_light of this InlineResponse2001.
        :rtype: float
        """
        return self._min_light

    @min_light.setter
    def min_light(self, min_light: float):
        """Sets the min_light of this InlineResponse2001.


        :param min_light: The min_light of this InlineResponse2001.
        :type min_light: float
        """

        self._min_light = min_light

    @property
    def max_light(self) -> float:
        """Gets the max_light of this InlineResponse2001.


        :return: The max_light of this InlineResponse2001.
        :rtype: float
        """
        return self._max_light

    @max_light.setter
    def max_light(self, max_light: float):
        """Sets the max_light of this InlineResponse2001.


        :param max_light: The max_light of this InlineResponse2001.
        :type max_light: float
        """

        self._max_light = max_light

    @property
    def min_humidity(self) -> float:
        """Gets the min_humidity of this InlineResponse2001.


        :return: The min_humidity of this InlineResponse2001.
        :rtype: float
        """
        return self._min_humidity

    @min_humidity.setter
    def min_humidity(self, min_humidity: float):
        """Sets the min_humidity of this InlineResponse2001.


        :param min_humidity: The min_humidity of this InlineResponse2001.
        :type min_humidity: float
        """

        self._min_humidity = min_humidity

    @property
    def max_humidity(self) -> float:
        """Gets the max_humidity of this InlineResponse2001.


        :return: The max_humidity of this InlineResponse2001.
        :rtype: float
        """
        return self._max_humidity

    @max_humidity.setter
    def max_humidity(self, max_humidity: float):
        """Sets the max_humidity of this InlineResponse2001.


        :param max_humidity: The max_humidity of this InlineResponse2001.
        :type max_humidity: float
        """

        self._max_humidity = max_humidity
