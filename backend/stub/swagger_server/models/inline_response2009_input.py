# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class InlineResponse2009Input(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, temp: float=None, humidity: float=None, wind_kph: float=None, width: float=None):  # noqa: E501
        """InlineResponse2009Input - a model defined in Swagger

        :param temp: The temp of this InlineResponse2009Input.  # noqa: E501
        :type temp: float
        :param humidity: The humidity of this InlineResponse2009Input.  # noqa: E501
        :type humidity: float
        :param wind_kph: The wind_kph of this InlineResponse2009Input.  # noqa: E501
        :type wind_kph: float
        :param width: The width of this InlineResponse2009Input.  # noqa: E501
        :type width: float
        """
        self.swagger_types = {
            'temp': float,
            'humidity': float,
            'wind_kph': float,
            'width': float
        }

        self.attribute_map = {
            'temp': 'temp',
            'humidity': 'humidity',
            'wind_kph': 'wind_kph',
            'width': 'width'
        }
        self._temp = temp
        self._humidity = humidity
        self._wind_kph = wind_kph
        self._width = width

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2009Input':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_9_input of this InlineResponse2009Input.  # noqa: E501
        :rtype: InlineResponse2009Input
        """
        return util.deserialize_model(dikt, cls)

    @property
    def temp(self) -> float:
        """Gets the temp of this InlineResponse2009Input.


        :return: The temp of this InlineResponse2009Input.
        :rtype: float
        """
        return self._temp

    @temp.setter
    def temp(self, temp: float):
        """Sets the temp of this InlineResponse2009Input.


        :param temp: The temp of this InlineResponse2009Input.
        :type temp: float
        """

        self._temp = temp

    @property
    def humidity(self) -> float:
        """Gets the humidity of this InlineResponse2009Input.


        :return: The humidity of this InlineResponse2009Input.
        :rtype: float
        """
        return self._humidity

    @humidity.setter
    def humidity(self, humidity: float):
        """Sets the humidity of this InlineResponse2009Input.


        :param humidity: The humidity of this InlineResponse2009Input.
        :type humidity: float
        """

        self._humidity = humidity

    @property
    def wind_kph(self) -> float:
        """Gets the wind_kph of this InlineResponse2009Input.


        :return: The wind_kph of this InlineResponse2009Input.
        :rtype: float
        """
        return self._wind_kph

    @wind_kph.setter
    def wind_kph(self, wind_kph: float):
        """Sets the wind_kph of this InlineResponse2009Input.


        :param wind_kph: The wind_kph of this InlineResponse2009Input.
        :type wind_kph: float
        """

        self._wind_kph = wind_kph

    @property
    def width(self) -> float:
        """Gets the width of this InlineResponse2009Input.


        :return: The width of this InlineResponse2009Input.
        :rtype: float
        """
        return self._width

    @width.setter
    def width(self, width: float):
        """Sets the width of this InlineResponse2009Input.


        :param width: The width of this InlineResponse2009Input.
        :type width: float
        """

        self._width = width
