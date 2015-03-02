#!/usr/bin/env python
# coding=utf-8

"""
An OPF `<itemref>` element, that is, a child of the `<spine>`.
"""

from yael.element import Element

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.6"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFItemref(Element):
    """
    Build an OPF `<itemref>` element or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    A_IDREF = "idref"
    A_LINEAR = "linear"
    A_PROPERTIES = "properties"
    V_PAGE_SPREAD_LEFT = "page-spread-left"
    V_PAGE_SPREAD_RIGHT = "page-spread-right"
    V_RENDITION_ALIGN_X_CENTER = "rendition:align-x-center"
    V_RENDITION_FLOW_AUTO = "rendition:flow-auto"
    V_RENDITION_FLOW_PAGINATED = "rendition:flow-paginated"
    V_RENDITION_FLOW_SCROLLED_CONTINUOUS = "rendition:flow-scrolled-continuous"
    V_RENDITION_FLOW_SCROLLED_DOC = "rendition:flow-scrolled-doc"
    V_RENDITION_LAYOUT_PRE_PAGINATED = "rendition:layout-pre-paginated"
    V_RENDITION_LAYOUT_REFLOWABLE = "rendition:layout-reflowable"
    V_RENDITION_ORIENTATION_AUTO = "rendition:orientation-auto"
    V_RENDITION_ORIENTATION_LANDSCAPE = "rendition:orientation-landscape"
    V_RENDITION_ORIENTATION_PORTRAIT = "rendition:orientation-portrait"
    V_RENDITION_PAGE_SPREAD_CENTER = "rendition:page-spread-center"
    V_RENDITION_SPREAD_AUTO = "rendition:spread-auto"
    V_RENDITION_SPREAD_BOTH = "rendition:spread-both"
    V_RENDITION_SPREAD_LANDSCAPE = "rendition:spread-landscape"
    V_RENDITION_SPREAD_NONE = "rendition:spread-none"
    V_RENDITION_SPREAD_PORTRAIT = "rendition:spread-portrait"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_id = None
        self.v_idref = None
        self.v_linear = None
        self.v_properties = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "id":         self.v_id,
            "idref":      self.v_idref,
            "linear":     self.v_linear,
            "properties": self.v_properties
        }
        return obj

    def parse_object(self, obj):
        # set attributes
        self.v_id = obj.get(OPFItemref.A_ID)
        self.v_idref = obj.get(OPFItemref.A_IDREF)
        self.v_linear = obj.get(OPFItemref.A_LINEAR)
        self.v_properties = obj.get(OPFItemref.A_PROPERTIES)

    def has_property(self, v_property):
        """
        Return True if this itemref has the given property.

        :param v_property: a property name
        :type  v_property: str
        :returns:          True if the itemref has the property
        :rtype:            bool

        """
        if self.v_properties != None:
            return v_property in self.v_properties.split(" ")
        return False

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
    def v_idref(self):
        """
        The value of the `idref` attribute.

        :rtype: str
        """
        return self.__v_idref

    @v_idref.setter
    def v_idref(self, v_idref):
        self.__v_idref = v_idref

    @property
    def v_linear(self):
        """
        The value of the `linear` attribute.

        :rtype: str
        """
        return self.__v_linear

    @v_linear.setter
    def v_linear(self, v_linear):
        self.__v_linear = v_linear

    @property
    def v_properties(self):
        """
        The value of the `properties` attribute.

        :rtype: str
        """
        return self.__v_properties

    @v_properties.setter
    def v_properties(self, v_properties):
        self.__v_properties = v_properties


