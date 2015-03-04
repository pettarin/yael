#!/usr/bin/env python
# coding=utf-8

"""
An NCX TOC tree.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.ncxtocnode import NCXTocNode
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.8"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class NCXToc(Element):
    """
    Build an NCX TOC tree or
    parse it from `obj` or `string`.
    """

    A_DTB_DEPTH = "dtb:depth"
    A_DTB_GENERATOR = "dtb:generator"
    A_DTB_MAXPAGENUMBER = "dtb:maxPageNumber"
    A_DTB_TOTALPAGECOUNT = "dtb:totalPageCount"
    A_DTB_UID = "dtb:uid"
    A_ID = "id"
    A_LANG = "lang"
    A_VERSION = "version"
    A_NS_LANG = "{{{0}}}{1}".format(Namespace.XML, A_LANG)
    E_DOCAUTHOR = "docAuthor"
    E_DOCTITLE = "docTitle"
    E_HEAD = "head"
    E_META = "meta"
    E_NAVMAP = "navMap"
    E_NAVPOINT = "navPoint"
    E_NCX = "ncx"
    E_TEXT = "text"

    # TODO split `<head>` into a separate class?

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_docauthor = None
        self.v_doctitle = None
        self.v_dtb_depth = None
        self.v_dtb_generator = None
        self.v_dtb_maxpagenumber = None
        self.v_dtb_totalpagecount = None
        self.v_dtb_uid = None
        self.v_id = None
        self.v_version = None
        self.v_xml_lang = None
        self.children = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "internal_path":      self.internal_path,
            "docauthor":          self.v_docauthor,
            "doctitle":           self.v_doctitle,
            "dtb_depth":          self.v_dtb_depth,
            "dtb_generator":      self.v_dtb_generator,
            "dtb_maxpagenumber":  self.v_dtb_maxpagenumber,
            "dtb_totalpagecount": self.v_dtb_totalpagecount,
            "dtb_uid":            self.v_dtb_uid,
            "id":                 self.v_id,
            "version":            self.v_version,
            "xml_lang":           self.v_xml_lang,
            "children":           len(self.children),
        }
        if recursive:
            obj["children"] = JSONAble.safe(self.children)
        return obj

    def parse_object(self, obj):
        # locate `<ncx>` element
        ncx_arr = yael.util.query_xpath(
            obj=obj,
            query="/{0}:{1}",
            args=['n', NCXToc.E_NCX],
            nsp={'n': Namespace.NCX, 'x': Namespace.XML},
            required=NCXToc.E_NCX)
        ncx = ncx_arr[0]

        self.v_id = ncx.get(NCXToc.A_ID)
        self.v_version = ncx.get(NCXToc.A_VERSION)
        self.v_xml_lang = ncx.get(NCXToc.A_NS_LANG)

        # locate `<meta>` element (if any)
        meta_arr = yael.util.query_xpath(
            obj=ncx,
            query="{0}:{1}/{0}:{2}",
            args=['n', NCXToc.E_HEAD, NCXToc.E_META],
            nsp={'n': Namespace.NCX},
            required=None)
        for meta in meta_arr:
            name = meta.get("name")
            content = meta.get("content")
            if name == NCXToc.A_DTB_UID:
                self.v_dtb_uid = content
            elif name == NCXToc.A_DTB_DEPTH:
                self.v_dtb_depth = content
            elif name == NCXToc.A_DTB_TOTALPAGECOUNT:
                self.v_dtb_totalpagecount = content
            elif name == NCXToc.A_DTB_MAXPAGENUMBER:
                self.v_dtb_maxpagenumber = content
            elif name == NCXToc.A_DTB_GENERATOR:
                self.v_dtb_generator = content

        # locate `<docTitle>` element (if any)
        doctitle_arr = yael.util.query_xpath(
            obj=ncx,
            query="{0}:{1}/{0}:{2}",
            args=['n', NCXToc.E_DOCTITLE, NCXToc.E_TEXT],
            nsp={'n': Namespace.NCX},
            required=None)
        if len(doctitle_arr) > 0:
            self.v_doctitle = doctitle_arr[0].text

        # locate `<docAuthor>` element (if any)
        docauthor_arr = yael.util.query_xpath(
            obj=ncx,
            query="{0}:{1}/{0}:{2}",
            args=['n', NCXToc.E_DOCAUTHOR, NCXToc.E_TEXT],
            nsp={'n': Namespace.NCX},
            required=None)
        if len(docauthor_arr) > 0:
            self.v_docauthor = docauthor_arr[0].text

        # locate `<navMap>` element (if any)
        navmap_arr = yael.util.query_xpath(
            obj=ncx,
            query="{0}:{1}",
            args=['n', NCXToc.E_NAVMAP],
            nsp={'n': Namespace.NCX},
            required=None)
        if len(navmap_arr) > 0:
            navmap = navmap_arr[0]

            # locate children `<navPoint>` elements (if any)
            navpoint_arr = yael.util.query_xpath(
                obj=navmap,
                query="{0}:{1}",
                args=['n', NCXToc.E_NAVPOINT],
                nsp={'n': Namespace.NCX},
                required=None)
            for navpoint in navpoint_arr:
                navpoint_parsed = None
                try:
                    navpoint_parsed = NCXTocNode(obj=navpoint)
                except:
                    pass
                if navpoint_parsed != None:
                    self.add_child(navpoint_parsed)

    def add_child(self, child):
        """
        Add the given child to this NCX TOC.

        :param child: the node child to be added
        :type  child: :class:`yael.ncxtocnode.NCXTocNode`

        """
        self.children.append(child)


    @property
    def v_docauthor(self):
        """
        The value of the `docAuthor` element.

        :rtype: str
        """
        return self.__v_docauthor

    @v_docauthor.setter
    def v_docauthor(self, v_docauthor):
        self.__v_docauthor = v_docauthor

    @property
    def v_doctitle(self):
        """
        The value of the `docTitle` element.

        :rtype: str
        """
        return self.__v_doctitle

    @v_doctitle.setter
    def v_doctitle(self, v_doctitle):
        self.__v_doctitle = v_doctitle

    @property
    def v_dtb_depth(self):
        """
        The value of the `dtb:depth` attribute.

        :rtype: str
        """
        return self.__v_dtb_depth

    @v_dtb_depth.setter
    def v_dtb_depth(self, v_dtb_depth):
        self.__v_dtb_depth = v_dtb_depth

    @property
    def v_dtb_generator(self):
        """
        The value of the `dtb:generator` attribute.

        :rtype: str
        """
        return self.__v_dtb_generator

    @v_dtb_generator.setter
    def v_dtb_generator(self, v_dtb_generator):
        self.__v_dtb_generator = v_dtb_generator

    @property
    def v_dtb_maxpagenumber(self):
        """
        The value of the `dtb:maxPageNumber` attribute.

        :rtype: str
        """
        return self.__v_dtb_maxpagenumber

    @v_dtb_maxpagenumber.setter
    def v_dtb_maxpagenumber(self, v_dtb_maxpagenumber):
        self.__v_dtb_maxpagenumber = v_dtb_maxpagenumber

    @property
    def v_dtb_totalpagecount(self):
        """
        The value of the `dtb:totalPageCount` attribute.

        :rtype: str
        """
        return self.__v_dtb_totalpagecount

    @v_dtb_totalpagecount.setter
    def v_dtb_totalpagecount(self, v_dtb_totalpagecount):
        self.__v_dtb_totalpagecount = v_dtb_totalpagecount

    @property
    def v_dtb_uid(self):
        """
        The value of the `dtb:uid` attribute.

        :rtype: str
        """
        return self.__v_dtb_uid

    @v_dtb_uid.setter
    def v_dtb_uid(self, v_dtb_uid):
        self.__v_dtb_uid = v_dtb_uid

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
    def v_version(self):
        """
        The value of the `version` attribute.

        :rtype: str
        """
        return self.__v_version

    @v_version.setter
    def v_version(self, v_version):
        self.__v_version = v_version

    @property
    def v_xml_lang(self):
        """
        The value of the `xml:lang` attribute.

        :rtype: str
        """
        return self.__v_xml_lang

    @v_xml_lang.setter
    def v_xml_lang(self, v_xml_lang):
        self.__v_xml_lang = v_xml_lang

    @property
    def children(self):
        """
        The children elements of this NCX TOC.

        :rtype: list of :class:`yael.ncxtocnode.NCXTocNode` objects
        """
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children


