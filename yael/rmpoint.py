#!/usr/bin/env python
# coding=utf-8

"""
An EPUB 3 Multiple Renditions Rendition Mapping Point.
"""

from yael.element import Element
from yael.namespace import Namespace

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class RMPoint(Element):
    """
    Build an EPUB 3 Multiple Renditions Rendition Mapping Point or
    parse it from `obj` or `string`.
    """

    A_HREF = "href"
    A_RENDITION = "rendition"
    A_NS_RENDITION = "{{{0}}}{1}".format(Namespace.EPUB, A_RENDITION)

    # TODO href might be an EPUB CFI => to be parsed...

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_epub_rendition = None
        self.v_href = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "epub_rendition": self.v_epub_rendition,
            "href":           self.v_href,
        }
        return obj

    def parse_object(self, obj):
        self.v_epub_rendition = obj.get(RMPoint.A_NS_RENDITION)
        self.v_href = obj.get(RMPoint.A_HREF)

    @property
    def v_epub_rendition(self):
        """
        The value of the `epub:rendition` attribute.

        :rtype: str
        """
        return self.__v_epub_rendition

    @v_epub_rendition.setter
    def v_epub_rendition(self, v_epub_rendition):
        self.__v_epub_rendition = v_epub_rendition

    @property
    def v_href(self):
        """
        The value of the `href` attribute.

        :rtype: str
        """
        return self.__v_href

    @v_href.setter
    def v_href(self, v_href):
        self.__v_href = v_href



