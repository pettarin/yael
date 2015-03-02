#!/usr/bin/env python
# coding=utf-8

"""
A `<nav>` element in the Navigation Document.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.navnode import NavNode
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.5"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class NavElement(Element):
    """
    Build a `<nav>` element in the Navigation Document
    or parse it from `obj` or `string`.
    """

    A_EPUB_TYPE = "type"
    A_ID = "id"
    A_NS_EPUB_TYPE = "{{{0}}}{1}".format(Namespace.EPUB, A_EPUB_TYPE)
    E_HX = ["h1", "h2", "h3", "h4", "h5", "h6"]
    E_LI = "li"
    E_OL = "ol"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_epub_type = None
        self.v_id = None
        self.children = []
        self.title = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "internal_path": self.internal_path,
            "epub_type":     self.v_epub_type,
            "id":            self.v_id,
            "children":      len(self.children),
            "title":         self.title,
        }
        if recursive:
            obj["children"] = JSONAble.safe(self.children)
        return obj

    def parse_object(self, obj):
        self.v_epub_type = obj.get(NavElement.A_NS_EPUB_TYPE)
        self.v_id = obj.get(NavElement.A_ID)

        # parse title (if any)
        # it can be any `<h1>` ... `<h6>` element
        for h_elem in NavElement.E_HX:
            h_arr = yael.util.query_xpath(
                obj=obj,
                query="{0}:{1}",
                args=["x", h_elem],
                nsp={"x": Namespace.XHTML},
                required=None)
            if len(h_arr) > 0:
                self.title = h_arr[0].xpath("string()")
                break

        # locate children `<ol><li>` elements (if any)
        li_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}/{0}:{2}",
            args=["x", NavElement.E_OL, NavElement.E_LI],
            nsp={"x": Namespace.XHTML},
            required=None)
        for li_elem in li_arr:
            li_parsed = None
            try:
                li_parsed = NavNode(obj=li_elem)
            except:
                pass
            if li_parsed != None:
                self.add_child(li_parsed)

    def add_child(self, child):
        """
        Add the given child to this `<nav>`.

        :param child: the node child to be added
        :type  child: :class:`yael.navnode.NavNode`

        """
        self.children.append(child)

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
    def v_epub_type(self):
        """
        The value of the `epub:type` attribute.

        :rtype: str
        """
        return self.__v_epub_type

    @v_epub_type.setter
    def v_epub_type(self, v_epub_type):
        self.__v_epub_type = v_epub_type

    @property
    def title(self):
        """
        The title of this `<nav>`.

        :rtype: str
        """
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def children(self):
        """
        The children elements of this `<nav>`.

        :rtype: list of :class:`yael.navnode.NavNode` objects
        """
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children


