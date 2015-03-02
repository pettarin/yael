#!/usr/bin/env python
# coding=utf-8

"""
An abstract Rendition, holding:

1. the Package Document (required)
2. the Navigation Document (required in EPUB 3)
3. the NCX TOC (EPUB 2, optional in EPUB 3)
4. the Media Overlay Documents (optional in EPUB 3)
5. the Multiple Rendition rendition:* properties (optional in EPUB 3)

"""

from yael.element import Element
from yael.jsonable import JSONAble

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.7"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Rendition(Element):
    """
    Build an abstract Rendition or
    parse it from `obj` or `string`.
    """

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_full_path = None
        self.v_media_type = None
        self.v_rendition_accessmode = None
        self.v_rendition_label = None
        self.v_rendition_language = None
        self.v_rendition_layout = None
        self.v_rendition_media = None
        self.mo_documents = []
        self.nav_document = None
        self.ncx_toc = None
        self.pac_document = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def parse_object(self, obj):
        pass

    def json_object(self, recursive=True):
        obj = {
            "full_path":            self.v_full_path,
            "media_type":           self.v_media_type,
            "rendition_accessmode": self.v_rendition_accessmode,
            "rendition_label":      self.v_rendition_label,
            "rendition_language":   self.v_rendition_language,
            "rendition_layout":     self.v_rendition_layout,
            "rendition_media":      self.v_rendition_media,
            "mo_documents":         len(self.mo_documents),
            "nav_document":         (self.nav_document == None),
            "ncx_toc":              (self.ncx_toc == None),
            "pac_document":         (self.pac_document == None),
        }
        if recursive:
            obj["mo_documents"] = JSONAble.safe(self.mo_documents)
            obj["nav_document"] = JSONAble.safe(self.nav_document)
            obj["ncx_toc"] = JSONAble.safe(self.ncx_toc)
            obj["pac_document"] = JSONAble.safe(self.pac_document)
        return obj

    def add_mo_document(self, mo_document):
        """
        Add the given Media Overlay Document to this Rendition.

        :param mo_document: the Media Overlay Document to be added
        :type  mo_document: :class:`yael.modocument.MODocument`

        """
        self.mo_documents.append(mo_document)

    @property
    def v_full_path(self):
        """
        The value of the `full-path` attribute.

        :rtype: str
        """
        return self.__v_full_path

    @v_full_path.setter
    def v_full_path(self, v_full_path):
        self.__v_full_path = v_full_path

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
    def v_rendition_accessmode(self):
        """
        The value of the `rendition:accessMode` attribute.

        :rtype: str
        """
        return self.__v_rendition_accessmode

    @v_rendition_accessmode.setter
    def v_rendition_accessmode(self, v_rendition_accessmode):
        self.__v_rendition_accessmode = v_rendition_accessmode

    @property
    def v_rendition_label(self):
        """
        The value of the `rendition:label` attribute.

        :rtype: str
        """
        return self.__v_rendition_label

    @v_rendition_label.setter
    def v_rendition_label(self, v_rendition_label):
        self.__v_rendition_label = v_rendition_label

    @property
    def v_rendition_language(self):
        """
        The value of the `rendition:language` attribute.

        :rtype: str
        """
        return self.__v_rendition_language

    @v_rendition_language.setter
    def v_rendition_language(self, v_rendition_language):
        self.__v_rendition_language = v_rendition_language

    @property
    def v_rendition_layout(self):
        """
        The value of the `rendition:layout` attribute.

        :rtype: str
        """
        return self.__v_rendition_layout

    @v_rendition_layout.setter
    def v_rendition_layout(self, v_rendition_layout):
        self.__v_rendition_layout = v_rendition_layout

    @property
    def v_rendition_media(self):
        """
        The value of the `rendition:media` attribute.

        :rtype: str
        """
        return self.__v_rendition_media

    @v_rendition_media.setter
    def v_rendition_media(self, v_rendition_media):
        self.__v_rendition_media = v_rendition_media

    @property
    def mo_documents(self):
        """
        The Media Overlay Documents associated with this Rendition.

        :rtype: list of :class:`yael.modocument.MODocument` objects
        """
        return self.__mo_documents

    @mo_documents.setter
    def mo_documents(self, mo_documents):
        self.__mo_documents = mo_documents

    @property
    def nav_document(self):
        """
        The Navigation Document associated with this Rendition,
        or None if not present.

        :rtype: :class:`yael.navdocument.NavDocument`
        """
        return self.__nav_document

    @nav_document.setter
    def nav_document(self, nav_document):
        self.__nav_document = nav_document

    @property
    def ncx_toc(self):
        """
        The NCX TOC associated with this Rendition,
        or None if not present.

        :rtype: :class:`yael.ncxtoc.NCXToc`
        """
        return self.__ncx_toc

    @ncx_toc.setter
    def ncx_toc(self, ncx_toc):
        self.__ncx_toc = ncx_toc

    @property
    def pac_document(self):
        """
        The Package Document associated with this Rendition,
        or None if not present.

        :rtype: :class:`yael.pacdocument.PacDocument`
        """
        return self.__pac_document

    @pac_document.setter
    def pac_document(self, pac_document):
        self.__pac_document = pac_document

    @property
    def toc(self):
        """
        The TOC associated with this Rendition.

        If the Rendition belongs to an EPUB 3 publication,
        return the `<nav>` TOC in the Navigation Document.

        If the Rendition belongs to an EPUB 2 publication,
        return the NCX TOC.

        If not present, return None.

        :rtype: :class:`yael.navelement.NavElement` or
                :class:`yael.ncxtoc.NCXToc`
        """
        try:
            return self.nav_document.toc
        except:
            pass
        if self.ncx_toc != None:
            return self.ncx_toc
        return None

    @property
    def landmarks(self):
        """
        The landmarks `<nav>` associated with this Rendition,
        or None if not present.

        :rtype: :class:`yael.navelement.NavElement`
        """
        try:
            return self.nav_document.landmarks
        except:
            pass
        return None


