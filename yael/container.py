#!/usr/bin/env python
# coding=utf-8

"""
The `META-INF/container.xml` file, storing:

1. the Rendition objects
2. the Rendition Mapping Document
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.mediatype import MediaType
from yael.namespace import Namespace
from yael.rendition import Rendition
from yael.rmdocument import RMDocument
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.8"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Container(Element):
    """
    Build the `META-INF/container.xml` file
    or parse it from `string` or `obj`.
    """

    A_ACCESSMODE = "accessMode"
    A_FULL_PATH = "full-path"
    A_HREF = "href"
    A_LABEL = "label"
    A_LANGUAGE = "language"
    A_LAYOUT = "layout"
    A_MEDIA = "media"
    A_MEDIA_TYPE = "media-type"
    A_MEDIA_TYPE = "media-type"
    A_REL = "rel"
    A_NS_ACCESSMODE = "{{{0}}}{1}".format(Namespace.RENDITION, A_ACCESSMODE)
    A_NS_LABEL = "{{{0}}}{1}".format(Namespace.RENDITION, A_LABEL)
    A_NS_LANGUAGE = "{{{0}}}{1}".format(Namespace.RENDITION, A_LANGUAGE)
    A_NS_LAYOUT = "{{{0}}}{1}".format(Namespace.RENDITION, A_LAYOUT)
    A_NS_MEDIA = "{{{0}}}{1}".format(Namespace.RENDITION, A_MEDIA)
    E_CONTAINER = "container"
    E_LINK = "link"
    E_ROOTFILE = "rootfile"
    E_ROOTFILES = "rootfiles"
    V_ACCESSMODE_AUDITORY = "auditory"
    V_ACCESSMODE_TACTILE = "tactile"
    V_ACCESSMODE_TEXTUAL = "textual"
    V_ACCESSMODE_VISUAL = "visual"
    V_LAYOUT_PRE_PAGINATED = "pre-paginated"
    V_LAYOUT_REFLOWABLE = "reflowable"
    V_REL_MAPPING = "mapping"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.renditions = []
        self.rm_document = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "internal_path": self.internal_path,
            "renditions":    len(self.renditions),
            "rm_document":   (self.rm_document == None),
        }
        if recursive:
            obj["renditions"] = JSONAble.safe(self.renditions)
            obj["rm_document"] = JSONAble.safe(self.rm_document)
        return obj

    def parse_object(self, obj):
        try:
            # locate `<container>` element
            container_arr = yael.util.query_xpath(
                obj=obj,
                query="/{0}:{1}",
                args=['c', Container.E_CONTAINER],
                nsp={'c': Namespace.CONTAINER},
                required=Container.E_CONTAINER)
            container = container_arr[0]

            # locate `<rootfile>` elements
            rootfile_arr = yael.util.query_xpath(
                obj=container,
                query="{0}:{1}/{0}:{2}",
                args=['c', Container.E_ROOTFILES, Container.E_ROOTFILE],
                nsp={'c': Namespace.CONTAINER},
                required=None)
            for rootfile in rootfile_arr:
                self._parse_rootfile(rootfile)

            # locate `<link>` optional element
            link_arr = yael.util.query_xpath(
                obj=container,
                query="{0}:{1}",
                args=['c', Container.E_LINK],
                nsp={'c': Namespace.CONTAINER},
                required=None)
            for link in link_arr:
                self._parse_link(link)
        except:
            raise Exception("Error while parsing the given object")

    def add_rendition(self, rendition):
        """
        Add a Rendition to this Container.

        :param rendition: Rendition to be added
        :type  rendition: :class:`yael.rendition.Rendition`

        """

        self.renditions.append(rendition)

    @property
    def renditions(self):
        """
        The list of Rendition objects in this Container.

        :rtype: list of :class:`yael.rendition.Rendition`
        """

        return self.__renditions

    @renditions.setter
    def renditions(self, renditions):
        self.__renditions = renditions

    @property
    def rm_document(self):
        """
        The Rendition Mapping Document object in this Container,
        or None if it is not present.

        :rtype: :class:`yael.rmdocument.RMDocument`
        """

        return self.__rm_document

    @rm_document.setter
    def rm_document(self, rm_document):
        self.__rm_document = rm_document

    @property
    def default_rendition(self):
        """
        The Default Rendition object in this Container,
        or None if there are no Renditions.

        :rtype: :class:`yael.rendition.Rendition`
        """

        return yael.util.safe_first(self.renditions)

    def _parse_rootfile(self, obj):
        """
        Parse the given `<rootfile>` node object,
        and append the parsed Rendition to this Container.
        """

        # required attributes
        full_path = obj.get(Container.A_FULL_PATH)
        media_type = obj.get(Container.A_MEDIA_TYPE)

        if (full_path != None) and (media_type != None):
            r_obj = Rendition(internal_path=full_path)
            r_obj.v_full_path = full_path
            r_obj.v_media_type = media_type

            # multiple renditions
            r_obj.v_rendition_accessmode = obj.get(Container.A_NS_ACCESSMODE)
            r_obj.v_rendition_label = obj.get(Container.A_NS_LABEL)
            r_obj.v_rendition_language = obj.get(Container.A_NS_LANGUAGE)
            r_obj.v_rendition_layout = obj.get(Container.A_NS_LAYOUT)
            r_obj.v_rendition_media = obj.get(Container.A_NS_MEDIA)

            self.renditions.append(r_obj)

    def _parse_link(self, obj):
        """
        Parse the given `<link>` node object,
        and append the parsed RMDocument
        to this Container.
        """

        # required attributes for rendition mapping document
        rel = obj.get(Container.A_REL)
        href = obj.get(Container.A_HREF)
        media_type = obj.get(Container.A_MEDIA_TYPE)
        if ((rel == Container.V_REL_MAPPING) and
                (media_type == MediaType.XHTML) and
                (href != None)):
            self.rm_document = RMDocument(internal_path=href)
        return None


