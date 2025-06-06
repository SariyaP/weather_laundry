# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.inline_response20013_input import InlineResponse20013Input  # noqa: F401,E501
from swagger_server import util


class InlineResponse20013(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, estimated_drying_time_hours: int=None, input: InlineResponse20013Input=None):  # noqa: E501
        """InlineResponse20013 - a model defined in Swagger

        :param estimated_drying_time_hours: The estimated_drying_time_hours of this InlineResponse20013.  # noqa: E501
        :type estimated_drying_time_hours: int
        :param input: The input of this InlineResponse20013.  # noqa: E501
        :type input: InlineResponse20013Input
        """
        self.swagger_types = {
            'estimated_drying_time_hours': int,
            'input': InlineResponse20013Input
        }

        self.attribute_map = {
            'estimated_drying_time_hours': 'estimated_drying_time_hours',
            'input': 'input'
        }
        self._estimated_drying_time_hours = estimated_drying_time_hours
        self._input = input

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse20013':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_13 of this InlineResponse20013.  # noqa: E501
        :rtype: InlineResponse20013
        """
        return util.deserialize_model(dikt, cls)

    @property
    def estimated_drying_time_hours(self) -> int:
        """Gets the estimated_drying_time_hours of this InlineResponse20013.


        :return: The estimated_drying_time_hours of this InlineResponse20013.
        :rtype: int
        """
        return self._estimated_drying_time_hours

    @estimated_drying_time_hours.setter
    def estimated_drying_time_hours(self, estimated_drying_time_hours: int):
        """Sets the estimated_drying_time_hours of this InlineResponse20013.


        :param estimated_drying_time_hours: The estimated_drying_time_hours of this InlineResponse20013.
        :type estimated_drying_time_hours: int
        """

        self._estimated_drying_time_hours = estimated_drying_time_hours

    @property
    def input(self) -> InlineResponse20013Input:
        """Gets the input of this InlineResponse20013.


        :return: The input of this InlineResponse20013.
        :rtype: InlineResponse20013Input
        """
        return self._input

    @input.setter
    def input(self, input: InlineResponse20013Input):
        """Sets the input of this InlineResponse20013.


        :param input: The input of this InlineResponse20013.
        :type input: InlineResponse20013Input
        """

        self._input = input
