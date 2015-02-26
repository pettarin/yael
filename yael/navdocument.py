#!/usr/bin/env python
# coding=utf-8

"""
A representation of the Navigation Document.

Basically, it is a collection of <nav> (NavElement) objects.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.navelement import NavElement
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class NavDocument(Element):
    """
    Build the Navigation Document or
    parse it from `obj` or `string`.
    """

    E_NAV = "nav"
    V_NAV_LANDMARKS = "landmarks"
    V_NAV_LOA = "loa"
    V_NAV_LOI = "loi"
    V_NAV_LOT = "lot"
    V_NAV_LOV = "lov"
    V_NAV_PAGE_LIST = "page-list"
    V_NAV_TOC = "toc"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.navs = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "internal_path": self.internal_path,
            "navs":          len(self.navs),
        }
        if recursive:
            obj["navs"] = JSONAble.safe(self.navs)
        return obj

    def parse_object(self, obj):
        nav_arr = yael.util.query_xpath(
            obj=obj,
            query="//{0}:{1}",
            args=["x", NavDocument.E_NAV],
            nsp={"x": Namespace.XHTML, "e": Namespace.EPUB},
            required=None)
        for nav in nav_arr:
            nav_parsed = None
            try:
                nav_parsed = NavElement(
                    internal_path=self.internal_path,
                    obj=nav)
            except:
                pass
            if nav_parsed != None:
                self.add_nav(nav_parsed)

    def add_nav(self, nav):
        """
        Add the given <nav> to this Navigation Document.

        :param nav: the <nav> to be added
        :type  nav: NavElement
        """
        self.navs.append(nav)

    @property
    def navs(self):
        """
        The list of <nav> objects in this Navigation Document.

        :rtype: list of :class:`yael.navelement.NavElement` objects
        """
        return self.__navs

    @navs.setter
    def navs(self, navs):
        self.__navs = navs

    def nav_by_id(self, v_id):
        """
        Return the <nav> child with given `id`.

        :param v_id: the desired `id`
        :type  v_id: str
        :returns:    the child with given id, or None if not found
        :rtype:      NavElement
        """
        lis = list(e for e in self.navs if e.v_id == v_id)
        return yael.util.safe_first(lis)

    def nav_by_epub_type(self, v_epub_type):
        """
        Return the <nav> child with given `epub:type`.

        :param v_epub_type: the desired `epub:type`
        :type  v_epub_type: str
        :returns:           the child with given epub:type,
                            or None if not found
        :rtype:             NavElement
        """
        lis = list(e for e in self.navs if e.v_epub_type == v_epub_type)
        return yael.util.safe_first(lis)

    @property
    def landmarks(self):
        """
        The landmarks <nav> element (None if not found).

        :rtype: :class:`yael.navelement.NavElement`
        """
        return self.nav_by_epub_type(NavDocument.V_NAV_LANDMARKS)

    @property
    def page_list(self):
        """
        The page-list <nav> element (None if not found).

        :rtype: :class:`yael.navelement.NavElement`
        """
        return self.nav_by_epub_type(NavDocument.V_NAV_PAGE_LIST)

    @property
    def toc(self):
        """
        The toc <nav> element (None if not found).

        :rtype: :class:`yael.navelement.NavElement`
        """
        return self.nav_by_epub_type(NavDocument.V_NAV_TOC)



