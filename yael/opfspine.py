#!/usr/bin/env python
# coding=utf-8

"""
The OPF `<spine>` element.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.opfitemref import OPFItemref
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.6"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFSpine(Element):
    """
    Build the OPF `<spine>` element or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    A_PAGE_PROGRESSION_DIRECTION = "page-progression-direction"
    A_TOC = "toc"
    E_ITEMREF = "itemref"
    V_NO = "no"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_id = None
        self.v_ppd = None
        self.v_toc = None
        self.itemrefs = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def parse_object(self, obj):
        # get attributes
        self.v_id = obj.get(OPFSpine.A_ID)
        self.v_ppd = obj.get(OPFSpine.A_PAGE_PROGRESSION_DIRECTION)
        self.v_toc = obj.get(OPFSpine.A_TOC)

        # locate `<itemref>` elements
        itemref_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}",
            args=["o", OPFSpine.E_ITEMREF],
            nsp={"o": Namespace.OPF, "x": Namespace.XML},
            required=None)
        for itemref in itemref_arr:
            itemref_parsed = None
            try:
                itemref_parsed = OPFItemref(obj=itemref)
            except:
                pass
            if itemref_parsed != None:
                self.add_itemref(itemref_parsed)

    def json_object(self, recursive=True):
        obj = {
            "id":                         self.v_id,
            "page_progression_direction": self.v_ppd,
            "toc":                        self.v_toc,
            "itemrefs":                   len(self.itemrefs)
        }
        if recursive:
            obj["itemrefs"] = JSONAble.safe(self.itemrefs)
        return obj

    def __len__(self):
        return len(self.itemrefs)

    def add_itemref(self, itemref):
        """
        Add the given `<itemref>` to the spine.

        :param item: the `<itemref>` to be added
        :type  item: :class:`yael.opfitemref.OPFItemref`
        """
        self.itemrefs.append(itemref)

    def itemref_by_id(self, v_id):
        """
        Return the `<itemref>` child with given `id`.

        :param v_id: the desired `id`
        :type  v_id: str
        :returns:    the child with given id, or None if not found
        :rtype:      :class:`yael.opfitemref.OPFItemref`
        """
        lis = list(e for e in self.itemrefs if e.v_id == v_id)
        return yael.util.safe_first(lis)

    def itemref_by_idref(self, v_idref):
        """
        Return the `<itemref>` child with given `idref`.

        :param v_idref: the desired `idref`
        :type  v_idref: str
        :returns:       the child with given id, or None if not found
        :rtype:         :class:`yael.opfitemref.OPFItemref`
        """
        lis = list(e for e in self.itemrefs if e.v_idref == v_idref)
        return yael.util.safe_first(lis)

    def index_by_idref(self, v_idref):
        """
        Return the index in the spine of the
        `<itemref>` child with given `idref`.

        :param v_idref: the desired `idref`
        :type  v_idref: str
        :returns:       the index, or -1 if not found
        :rtype:         int
        """
        index = 0
        for itemref in self.itemrefs:
            if itemref.v_idref == v_idref:
                return index
            index += 1
        return -1

    def linear_index_by_idref(self, v_idref):
        """
        Return the index in the linear spine of the
        `<itemref>` child with given `idref`.

        :param v_idref: the desired `idref`
        :type  v_idref: str
        :returns:       the index, or -1 if not found
        :rtype:         int
        """
        index = 0
        for itemref in self.linear_itemrefs:
            if itemref.v_idref == v_idref:
                return index
            index += 1
        return -1

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
    def v_ppd(self):
        """
        The value of the `page-progression-direction` attribute.

        :rtype: str
        """
        return self.__v_ppd

    @v_ppd.setter
    def v_ppd(self, v_ppd):
        self.__v_ppd = v_ppd

    @property
    def v_toc(self):
        """
        The value of the `toc` attribute.

        :rtype: str
        """
        return self.__v_toc

    @v_toc.setter
    def v_toc(self, v_toc):
        self.__v_toc = v_toc

    @property
    def itemrefs(self):
        """
        The list of `<itemref>` objects in this spine.

        :rtype: list of :class:`yael.opfitemref.OPFItemref` objects
        """
        return self.__itemrefs

    @itemrefs.setter
    def itemrefs(self, itemrefs):
        self.__itemrefs = itemrefs

    @property
    def linear_itemrefs(self):
        """
        The list of `<itemref>` objects in this spine,
        with `linear="yes"` (or omitted) attribute.

        :rtype: list of :class:`yael.opfitemref.OPFItemref` objects
        """
        return list(e for e in self.itemrefs if e.v_linear != OPFSpine.V_NO)


