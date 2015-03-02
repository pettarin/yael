#!/usr/bin/env python
# coding=utf-8

"""
An OPF `<reference>` element, that is, a child of the `<guide>`.
"""

from yael.element import Element

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.6"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFReference(Element):
    """
    Build an OPF `<reference>` element or
    parse it from `obj` or `string`.
    """

    A_HREF = "href"
    A_ID = "id"
    A_TITLE = "title"
    A_TYPE = "type"
    V_ACKNOWLEDGEMENTS = "acknowledgements"
    V_BIBLIOGRAPHY = "bibliography"
    V_COLOPHON = "colophon"
    V_COPYRIGHT_PAGE = "copyright-page"
    V_COVER = "cover"
    V_DEDICATION = "dedication"
    V_EPIGRAPH = "epigraph"
    V_FOREWORD = "foreword"
    V_GLOSSARY = "glossary"
    V_INDEX = "index"
    V_LOI = "loi"
    V_LOT = "lot"
    V_NOTES = "notes"
    V_PREFACE = "preface"
    V_TEXT = "text"
    V_TITLE_PAGE = "title-page"
    V_TOC = "toc"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_href = None
        self.v_id = None
        self.v_title = None
        self.v_type = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "href":  self.v_href,
            "id":    self.v_id,
            "title": self.v_title,
            "type":  self.v_type,
        }
        return obj

    def parse_object(self, obj):
        self.v_href = obj.get(OPFReference.A_HREF)
        self.v_id = obj.get(OPFReference.A_ID)
        self.v_title = obj.get(OPFReference.A_TITLE)
        self.v_type = obj.get(OPFReference.A_TYPE)

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
    def v_title(self):
        """
        The value of the `title` attribute.

        :rtype: str
        """
        return self.__v_title

    @v_title.setter
    def v_title(self, v_title):
        self.__v_title = v_title

    @property
    def v_type(self):
        """
        The value of the `type` attribute.

        :rtype: str
        """
        return self.__v_type

    @v_type.setter
    def v_type(self, v_type):
        self.__v_type = v_type


