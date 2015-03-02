#!/usr/bin/env python
# coding=utf-8

"""
A node in a NCX TOC tree.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.5"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class NCXTocNode(Element):
    """
    Build a node in a NCX TOC tree or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    A_PLAYORDER = "playOrder"
    A_SRC = "src"
    E_CONTENT = "content"
    E_NAVLABEL = "navLabel"
    E_NAVPOINT = "navPoint"
    E_TEXT = "text"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_id = None
        self.v_play_order = None
        self.v_src = None
        self.v_text = None
        self.children = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "id":        self.v_id,
            "playorder": self.v_play_order,
            "src":       self.v_src,
            "text":      self.v_text,
            "children":  len(self.children),
        }
        if recursive:
            obj["children"] = JSONAble.safe(self.children)
        return obj


    def parse_object(self, obj):
        # set id and play_order attributes
        self.v_id = obj.get(NCXTocNode.A_ID)
        self.v_play_order = obj.get(NCXTocNode.A_PLAYORDER)

        # set text (if any)
        text_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}/{0}:{2}",
            args=['n', NCXTocNode.E_NAVLABEL, NCXTocNode.E_TEXT],
            nsp={'n': Namespace.NCX},
            required=None)
        if len(text_arr) > 0:
            self.v_text = yael.util.safe_strip(text_arr[0].text)

        # set src (if any)
        content_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}",
            args=['n', NCXTocNode.E_CONTENT],
            nsp={'n': Namespace.NCX},
            required=None)
        if len(content_arr) > 0:
            self.v_src = content_arr[0].get(NCXTocNode.A_SRC)

        # locate children `<navPoint>` elements (if any)
        nav_points_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}",
            args=['n', NCXTocNode.E_NAVPOINT],
            nsp={'n': Namespace.NCX},
            required=None)
        for nav_point in nav_points_arr:
            nav_point_parsed = None
            try:
                nav_point_parsed = NCXTocNode(obj=nav_point)
            except:
                pass
            if nav_point_parsed != None:
                self.children.append(nav_point_parsed)

    def add_child(self, child):
        """
        Add the given child to this node.

        :param child: the node child to be added
        :type  child: :class:`yael.ncxtocnode.NCXTocNode`

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
    def v_src(self):
        """
        The value of the `src` attribute.

        :rtype: str
        """
        return self.__v_src

    @v_src.setter
    def v_src(self, v_src):
        self.__v_src = v_src

    @property
    def v_text(self):
        """
        The value of the `text` attribute.

        :rtype: str
        """
        return self.__v_text

    @v_text.setter
    def v_text(self, v_text):
        self.__v_text = v_text

    @property
    def v_play_order(self):
        """
        The value of the `playOrder` attribute.

        :rtype: str
        """
        return self.__v_play_order

    @v_play_order.setter
    def v_play_order(self, v_play_order):
        self.__v_play_order = v_play_order

    @property
    def children(self):
        """
        The children elements of this node.

        :rtype: list of :class:`yael.ncxtocnode.NCXTocNode` objects
        """
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children


