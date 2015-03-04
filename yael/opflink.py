#!/usr/bin/env python
# coding=utf-8

"""
An OPF `<link>` element, that is, a child of the `<metadata>`.
"""

from yael.element import Element

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.8"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFLink(Element):
    """
    Build an OPF `<link>` element or
    parse it from `obj` or `string`.
    """

    A_HREF = "href"
    A_ID = "id"
    A_MEDIA_TYPE = "media-type"
    A_REFINES = "refines"
    A_REL = "rel"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_href = None
        self.v_id = None
        self.v_media_type = None
        self.v_refines = None
        self.v_rel = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "href":       self.v_href,
            "id":         self.v_id,
            "media-type": self.v_media_type,
            "refines":    self.v_refines,
            "rel":        self.v_rel,
        }
        return obj

    def parse_object(self, obj):
        self.v_href = obj.get(OPFLink.A_HREF)
        self.v_id = obj.get(OPFLink.A_ID)
        self.v_media_type = obj.get(OPFLink.A_MEDIA_TYPE)
        self.v_refines = obj.get(OPFLink.A_REFINES)
        self.v_rel = obj.get(OPFLink.A_REL)

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
    def v_refines(self):
        """
        The value of the `refines` attribute.

        :rtype: str
        """
        return self.__v_refines

    @v_refines.setter
    def v_refines(self, v_refines):
        self.__v_refines = v_refines

    @property
    def v_rel(self):
        """
        The value of the `rel` attribute.

        :rtype: str
        """
        return self.__v_rel

    @v_rel.setter
    def v_rel(self, v_rel):
        self.__v_rel = v_rel


