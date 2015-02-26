#!/usr/bin/env python
# coding=utf-8

"""
A Media Overlay <text> element.
"""

from yael.element import Element

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class MOText(Element):
    """
    Build a Media Overlay <text> element or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    A_SRC = "src"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_id = None
        self.v_src = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "id":  self.v_id,
            "src": self.v_src
        }
        return obj

    def parse_object(self, obj):
        self.v_id = obj.get(MOText.A_ID)
        self.v_src = obj.get(MOText.A_SRC)

    @property
    def v_id(self):
        """
        The value of the `id` attribute.

        :rtype: str
        """
        return self.__v_id

    @v_id.setter
    def v_id(self, v_id):
        self.__v_id = v_id

    @property
    def v_src(self):
        """
        The value of the `src` attribute.

        :rtype: str
        """
        return self.__v_src

    @v_src.setter
    def v_src(self, v_src):
        self.__v_src = v_src



