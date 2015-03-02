#!/usr/bin/env python
# coding=utf-8

"""
A `<li>` node inside a `<nav>` tree.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.7"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class NavNode(Element):
    """
    Build a `<li>` node inside a `<nav>` tree or
    parse it from `obj` or `string`.
    """

    A_EPUB_TYPE = "type"
    A_HREF = "href"
    A_ID = "id"
    A_NS_EPUB_TYPE = "{{{0}}}{1}".format(Namespace.EPUB, A_EPUB_TYPE)
    E_A = "a"
    E_LI = "li"
    E_OL = "ol"
    E_SPAN = "span"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_epub_type = None
        self.v_href = None
        self.v_id = None
        self.v_label = None
        self.children = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "epub_type": self.v_epub_type,
            "href":      self.v_href,
            "id":        self.v_id,
            "label":     self.v_label,
            "children":  len(self.children),
        }
        if recursive:
            obj["children"] = JSONAble.safe(self.children)
        return obj

    def parse_object(self, obj):
        # locate `<span>` element (if any)
        span_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}",
            args=["x", NavNode.E_SPAN],
            nsp={"x": Namespace.XHTML},
            required=None)
        if len(span_arr) > 0:
            span_elem = span_arr[0]
            self.v_label = span_elem.xpath("string()")
            self.v_id = span_elem.get(NavNode.A_ID)

        # locate `<a>` element (if any)
        a_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}",
            args=["x", NavNode.E_A],
            nsp={"x": Namespace.XHTML},
            required=None)
        if len(a_arr) > 0:
            a_elem = a_arr[0]
            self.v_label = a_elem.xpath("string()")
            self.v_id = a_elem.get(NavNode.A_ID)
            self.v_href = a_elem.get(NavNode.A_HREF)
            self.v_epub_type = a_elem.get(NavNode.A_NS_EPUB_TYPE)

        # locate children `<ol><li>` elements (if any)
        li_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}/{0}:{2}",
            args=["x", NavNode.E_OL, NavNode.E_LI],
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
        Add the given child to this node.

        :param child: the node child to be added
        :type  child: :class:`yael.navnode.NavNode`

        """
        self.children.append(child)

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
    def v_href(self):
        """
        The value of the `href` attribute.

        :rtype: str
        """
        return self.__v_href

    @v_href.setter
    def v_href(self, v_href):
        self.__v_href = v_href

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
    def v_label(self):
        """
        The label of this node.

        :rtype: str
        """
        return self.__v_label

    @v_label.setter
    def v_label(self, v_label):
        self.__v_label = v_label

    @property
    def children(self):
        """
        The children elements.

        :rtype: list of :class:`yael.navnode.NavNode`
        """
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children


