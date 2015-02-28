#!/usr/bin/env python
# coding=utf-8

"""
An OPF `<item>` element, that is, a child of the `<manifest>`.
"""

from yael.element import Element
from yael.jsonable import JSONAble

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.2"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFItem(Element):
    """
    Build an OPF `<item>` element or
    parse it from `obj` or `string`.
    """

    A_FALLBACK = "fallback"
    A_HREF = "href"
    A_ID = "id"
    A_MEDIA_OVERLAY = "media-overlay"
    A_MEDIA_TYPE = "media-type"
    A_PROPERTIES = "properties"
    V_COVER_IMAGE = "cover-image"
    V_MATHML = "mathml"
    V_NAV = "nav"
    V_REMOTE_RESOURCES = "remote-resources"
    V_SCRIPTED = "scripted"
    V_SVG = "svg"
    V_SWITCH = "switch"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_fallback = None
        self.v_href = None
        self.v_id = None
        self.v_media_overlay = None
        self.v_media_type = None
        self.v_properties = None
        self.refinements = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "fallback":      self.v_fallback,
            "href":          self.v_href,
            "id":            self.v_id,
            "media_overlay": self.v_media_overlay,
            "media_type":    self.v_media_type,
            "properties":    self.v_properties,
            "refinements":   len(self.refinements),
        }
        if recursive:
            obj["refinements"] = JSONAble.safe(self.refinements)
        return obj

    def parse_object(self, obj):
        self.v_fallback = obj.get(OPFItem.A_FALLBACK)
        self.v_href = obj.get(OPFItem.A_HREF)
        self.v_id = obj.get(OPFItem.A_ID)
        self.v_media_overlay = obj.get(OPFItem.A_MEDIA_OVERLAY)
        self.v_media_type = obj.get(OPFItem.A_MEDIA_TYPE)
        self.v_properties = obj.get(OPFItem.A_PROPERTIES)

    def add_refinement(self, refinement):
        """
        Add a refinement, that is,
        store a reference to the refinement metadatum.

        :param refinement: the refinement metadatum
        :type  refinement: :class:`yael.opfmetadatum.OPFMetadatum`

        """
        self.refinements.append(refinement)

    def has_property(self, v_property):
        """
        Return True if this item has the given property.

        :param v_property: a property name
        :type  v_property: str
        :returns:          True if the item has the property
        :rtype:            bool

        """

        if self.v_properties != None:
            return v_property in self.v_properties.split(" ")
        return False

    @property
    def v_fallback(self):
        """
        The value of the `fallback` attribute.

        :rtype: str
        """
        return self.__v_fallback

    @v_fallback.setter
    def v_fallback(self, v_fallback):
        self.__v_fallback = v_fallback

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
    def v_media_overlay(self):
        """
        The value of the `media-overlay` attribute.

        :rtype: str
        """
        return self.__v_media_overlay

    @v_media_overlay.setter
    def v_media_overlay(self, v_media_overlay):
        self.__v_media_overlay = v_media_overlay

    @property
    def v_media_type(self):
        """
        The value of the `media-type` attribute.

        :rtype: str
        """
        return self.__v_media_type

    @v_media_type.setter
    def v_media_type(self, v_media_type):
        self.__v_media_type = v_media_type

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



