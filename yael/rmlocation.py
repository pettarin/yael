#!/usr/bin/env python
# coding=utf-8

"""
An EPUB 3 Multiple Renditions Rendition Mapping Location.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.rmpoint import RMPoint
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.2"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class RMLocation(Element):
    """
    Build an EPUB 3 Multiple Renditions Rendition Mapping Location or
    parse it from `obj` or `string`.
    """

    E_A = "a"
    E_LI = "li"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.points = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "points": len(self.points),
        }
        if recursive:
            obj["points"] = JSONAble.safe(self.points)
        return obj

    def parse_object(self, obj):
        try:
            # locate `<li><a>` elements
            a_arr = yael.util.query_xpath(
                obj=obj,
                query="{0}:{1}/{0}:{2}",
                args=[
                    "x",
                    RMLocation.E_LI,
                    RMLocation.E_A],
                nsp={"x": Namespace.XHTML},
                required=None)
            if len(a_arr) > 0:
                for a_elem in a_arr:
                    try:
                        a_parsed = RMPoint(obj=a_elem)
                        self.add_point(a_parsed)
                    except:
                        pass
        except:
            raise Exception("Error while parsing the given object")

    def add_point(self, point):
        """
        Add the given Rendition Mapping Point to this Location.

        :param point: the location point to be added
        :type  point: :class:`yael.rmpoint.RMPoint`

        """
        self.points.append(point)

    @property
    def points(self):
        """
        The Rendition Mapping Point objects in this Location.

        :rtype: list of :class:`yael.rmpoint.RMPoint` objects
        """
        return self.__points

    @points.setter
    def points(self, points):
        self.__points = points



