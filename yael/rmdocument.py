#!/usr/bin/env python
# coding=utf-8

"""
The EPUB 3 Multiple Renditions Rendition Mapping Document.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.rmlocation import RMLocation
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.5"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class RMDocument(Element):
    """
    Build the EPUB 3 Multiple Renditions Rendition Mapping Document or
    parse it from `obj` or `string`.
    """

    A_TYPE = "type"
    A_NS_TYPE = "{{{0}}}{1}".format(Namespace.EPUB, A_TYPE)
    E_BODY = "body"
    E_HEAD = "head" # TODO currently not parsed
    E_HTML = "html"
    E_META = "meta" # TODO currently not parsed
    E_NAV = "nav"
    E_UL = "ul"
    V_RESOURCE_MAP = "resource-map"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_epub_type = None
        self.locations = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "internal_path": self.internal_path,
            "epub_type":     self.v_epub_type,
            "locations":     len(self.locations),
        }
        if recursive:
            obj["locations"] = JSONAble.safe(self.locations)
        return obj

    def parse_object(self, obj):
        try:
            # locate `<nav>` element
            nav_arr = yael.util.query_xpath(
                obj=obj,
                query="/{0}:{1}/{0}:{2}/{0}:{3}",
                args=[
                    'x',
                    RMDocument.E_HTML,
                    RMDocument.E_BODY,
                    RMDocument.E_NAV],
                nsp={'x': Namespace.XHTML},
                required=RMDocument.E_NAV)
            nav = nav_arr[0]

            # check we have the correct type
            epub_type = nav.get(RMDocument.A_NS_TYPE)
            if epub_type == RMDocument.V_RESOURCE_MAP:
                self.v_epub_type = epub_type

                # locate `<ul>` elements
                ul_arr = yael.util.query_xpath(
                    obj=nav,
                    query="{0}:{1}",
                    args=['x', RMDocument.E_UL],
                    nsp={'x': Namespace.XHTML},
                    required=None)
                for ul_element in ul_arr:
                    ul_parsed = None
                    try:
                        ul_parsed = RMLocation(obj=ul_element)
                        self.add_location(ul_parsed)
                    except:
                        pass
        except:
            raise Exception("Error while parsing the given object")

    def add_location(self, location):
        """
        Add the given Rendition Mapping Location to this document.

        :param location: the location to be added
        :type  location: :class:`yael.rmlocation.RMLocation`

        """
        self.locations.append(location)

    @property
    def locations(self):
        """
        The Rendition Mapping Location objects in this document.

        :rtype: list of :class:`yael.rmlocation.RMLocation`
        """
        return self.__locations

    @locations.setter
    def locations(self, locations):
        self.__locations = locations

    @property
    def v_epub_type(self):
        """
        The value of the `epub:type` attribute.

        :rtype: str
        """
        return self.__v_epub_type

    @v_epub_type.setter
    def v_epub_type(self, v_epub_type):
        self.__v_epub_type = v_epub_type


