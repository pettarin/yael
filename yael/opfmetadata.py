#!/usr/bin/env python
# coding=utf-8

"""
The OPF `<metadata>` element.
"""

from yael.dc import DC
from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.opflink import OPFLink
from yael.opfdc import OPFDC
from yael.opfmeta2 import OPFMeta2
from yael.opfmeta3 import OPFMeta3
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.4"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFMetadata(Element):
    """
    Build the OPF `<metadata>` element or
    parse it from `obj` or `string`.
    """

    A_CONTENT = "content"
    A_DIR = "dir"
    A_ID = "id"
    A_LANG = "lang"
    A_NAME = "name"
    A_PROPERTY = "property"
    A_REFINES = "refines"
    A_SCHEME = "scheme"
    A_NS_LANG = "{{{0}}}{1}".format(Namespace.XML, A_LANG)
    E_LINK = "link"
    E_META = "meta"
    E_NS_META = "{{{0}}}{1}".format(Namespace.OPF, E_META)

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_dir = None
        self.v_id = None
        self.v_xml_lang = None
        self.links = []
        self.metadata = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def parse_object(self, obj):
        self.v_id = obj.get(OPFMetadata.A_ID)
        self.v_dir = obj.get(OPFMetadata.A_DIR)
        self.v_xml_lang = obj.get(OPFMetadata.A_NS_LANG)

        # locate `<dc:...>` elements
        for element in DC.ALL_ELEMENTS:
            dc_arr = yael.util.query_xpath(
                obj=obj,
                query="{0}:{1}",
                args=["dc", element],
                nsp={"dc": Namespace.DC, "x": Namespace.XML},
                required=None)
            for dc_elem in dc_arr:
                dc_elem_parsed = None
                try:
                    dc_elem_parsed = OPFDC(obj=dc_elem)
                except:
                    pass
                if dc_elem_parsed != None:
                    self.add_metadatum(dc_elem_parsed)

        # locate `<meta>` elements
        meta_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}",
            args=["o", OPFMetadata.E_META],
            nsp={"o": Namespace.OPF, "x": Namespace.XML},
            required=None)
        for meta in meta_arr:
            meta_parsed = None
            try:
                prop = meta.get(OPFMetadata.A_PROPERTY)
                if prop == None:
                    meta_parsed = OPFMeta2(obj=meta)
                else:
                    meta_parsed = OPFMeta3(obj=meta)
            except:
                pass
            if meta_parsed != None:
                self.add_metadatum(meta_parsed)

        # locate `<link>` elements
        link_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}",
            args=["o", OPFMetadata.E_LINK],
            nsp={"o": Namespace.OPF, "x": Namespace.XML},
            required=None)
        for link in link_arr:
            link_parsed = None
            try:
                link_parsed = OPFLink(obj=link)
            except:
                pass
            if link_parsed != None:
                self.add_link(link_parsed)

    def json_object(self, recursive=True):
        obj = {
            "dir":      self.v_dir,
            "id":       self.v_id,
            "xml_lang": self.v_xml_lang,
            "links":    len(self.links),
            "metadata": len(self.metadata),
        }
        if recursive:
            obj["links"] = JSONAble.safe(self.links)
            obj["metadata"] = JSONAble.safe(self.metadata)
        return obj

    def metadatum_by_id(self, v_id):
        """
        Return the metadatum child with given `id`.

        :param v_id: the desired `id`
        :type  v_id: str
        :returns:    the child with given id, or None if not found
        :rtype:      :class:`yael.opfmetadatum.OPFMetadatum`
        """
        lis = list(e for e in self.metadata if e.v_id == v_id)
        return yael.util.safe_first(lis)

    def metadata_by_tag(self, v_tag):
        """
        Return the metadata with `<tag>`.

        :param v_tag: the desired `tag`
        :type  v_tag: str
        :returns:     the list of OPFMetadatum items with given tag
        :rtype:       list of :class:`yael.opfmetadatum.OPFMetadatum`
        """
        return list(e for e in self.metadata if e.v_tag == v_tag)

    def metadata_by_property(self, v_property):
        """
        Return the metadatum child with given `prop` property.

        :param v_property: the desired `prop` property
        :type  v_property: str
        :returns:          the list of OPFMetadatum items with given property
        :rtype:            list of :class:`yael.opfmetadatum.OPFMetadatum`
        """
        return list(e for e in self.metadata if (
            isinstance(e, OPFMeta3) and (e.v_property == v_property)))

    def add_metadatum(self, metadatum):
        """
        Add the given metadatum to the metadata.

        :param metadatum: the metadatum to be added
        :type  metadatum: :class:`yael.opfmetadatum.OPFMetadatum`
        """
        self.metadata.append(metadatum)

    def add_link(self, link):
        """
        Add the given `<link>` to the metadata.

        :param link: the `<link>` to be added
        :type  link: :class:`yael.opflink.OPFLink`
        """
        self.links.append(link)

    @property
    def cover_image_item_id(self):
        """
        The value of the `id` attribute of the cover image item.

        :rtype: str
        """

        for metadatum in self.metadata:
            if (isinstance(metadatum, OPFMeta2) and
                    (metadatum.v_name == OPFMeta2.V_COVER)):
                return  metadatum.v_content
        return None

    @property
    def dcterms_modified(self):
        """
        The value of the `dcterms:modified` date.

        :rtype: str
        """
        for metadatum in self.metadata:
            if (isinstance(metadatum, OPFMeta3) and
                    (metadatum.v_property == DC.V_DCTERMS_MODIFIED)):
                return  metadatum.v_text
        return None

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
    def v_dir(self):
        """
        The value of the `dir` attribute.

        :rtype: str
        """
        return self.__v_dir

    @v_dir.setter
    def v_dir(self, v_dir):
        self.__v_dir = v_dir

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
    def metadata(self):
        """
        The list of metadatum objects.

        :rtype: list of :class:`yael.opfmetadatum.OPFMetadatum` objects
        """
        return self.__metadata

    @metadata.setter
    def metadata(self, metadata):
        self.__metadata = metadata

    @property
    def links(self):
        """
        The list of `<link>` objects.

        :rtype: list of :class:`yael.opflink.OPFLink` objects
        """
        return self.__links

    @links.setter
    def links(self, links):
        self.__links = links



