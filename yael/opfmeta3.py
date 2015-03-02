#!/usr/bin/env python
# coding=utf-8

"""
An OPF `<meta>` EPUB 3 metadatum, child of `<metadata>`.
"""

from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.opfmetadatum import OPFMetadatum
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.7"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFMeta3(OPFMetadatum):
    """
    Build an OPF `<meta>` EPUB 3 metadatum or
    parse it from `obj` or `string`.
    """

    A_DIR = "dir"
    A_ID = "id"
    A_LANG = "lang"
    A_PROPERTY = "property"
    A_REFINES = "refines"
    A_SCHEME = "scheme"
    A_NS_LANG = "{{{0}}}{1}".format(Namespace.XML, A_LANG)
    V_ALTERNATE_SCRIPT = "alternate-script"
    V_BELONGS_TO_COLLECTION = "belongs-to-collection"
    V_COLLECTION_TYPE = "collection-type"
    V_COLLECTION_TYPE_SERIES = "series"
    V_COLLECTION_TYPE_SET = "set"
    V_DISPLAY_SEQ = "display-seq"
    V_FILE_AS = "file-as"
    V_GROUP_POSITION = "group-position"
    V_IDENTIFIER_TYPE = "identifier-type"
    V_MEDIA_ACTIVE_CLASS = "media:active-class"
    V_MEDIA_DURATION = "media:duration"
    V_MEDIA_NARRATOR = "media:narrator"
    V_MEDIA_PAUSED_CLASS = "media:paused-class"
    V_MEDIA_PLAYBACK_ACTIVE_CLASS = "media:playback-active-class"
    V_META_AUTH = "meta-auth"
    V_ORIENTATION_AUTO = "auto"
    V_ORIENTATION_LANDSCAPE = "landscape"
    V_ORIENTATION_PORTRAIT = "portrait"
    V_RENDITION_FLOW = "rendition:flow"
    V_RENDITION_FLOW_AUTO = "auto"
    V_RENDITION_FLOW_PAGINATED = "paginated"
    V_RENDITION_FLOW_SCROLLED_CONTINUOUS = "scrolled-continuous"
    V_RENDITION_FLOW_SCROLLED_DOC = "scrolled-doc"
    V_RENDITION_LAYOUT = "rendition:layout"
    V_RENDITION_LAYOUT_PRE_PAGINATED = "pre-paginated"
    V_RENDITION_LAYOUT_REFLOWABLE = "reflowable"
    V_RENDITION_ORIENTATION = "rendition:orientation"
    V_RENDITION_SPREAD = "rendition:spread"
    V_RENDITION_SPREAD_AUTO = "auto"
    V_RENDITION_SPREAD_BOTH = "both"
    V_RENDITION_SPREAD_LANDSCAPE = "landscape"
    V_RENDITION_SPREAD_NONE = "none"
    V_RENDITION_SPREAD_PORTRAIT = "portrait"
    V_RENDITION_VIEWPORT = "rendition:viewport"
    V_ROLE = "role"
    V_SOURCE_OF = "source-of"
    V_SOURCE_OF_PAGINATION = "pagination"
    V_TITLE_TYPE = "title-type"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_dir = None
        self.v_id = None
        self.v_property = None
        self.v_refines = None
        self.v_scheme = None
        self.v_tag = None
        self.v_text = None
        self.v_xml_lang = None
        OPFMetadatum.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "dir":         self.v_dir,
            "id":          self.v_id,
            "property":    self.v_property,
            "refines":     self.v_refines,
            "scheme":      self.v_scheme,
            "tag":         self.v_tag,
            "text":        self.v_text,
            "xml_lang":    self.v_xml_lang,
            "refinements": len(self.refinements),
        }
        if recursive:
            obj["refinements"] = JSONAble.safe(self.refinements)
        return obj

    def parse_object(self, obj):
        self.v_dir = obj.get(OPFMeta3.A_DIR)
        self.v_id = obj.get(OPFMeta3.A_ID)
        self.v_property = obj.get(OPFMeta3.A_PROPERTY)
        self.v_refines = obj.get(OPFMeta3.A_REFINES)
        self.v_scheme = obj.get(OPFMeta3.A_SCHEME)
        self.v_tag = obj.tag
        self.v_text = yael.util.safe_strip(obj.text)
        self.v_xml_lang = obj.get(OPFMeta3.A_NS_LANG)

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
    def v_property(self):
        """
        The value of the `property` attribute.

        :rtype: str
        """
        return self.__v_property

    @v_property.setter
    def v_property(self, v_property):
        self.__v_property = v_property

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
    def v_scheme(self):
        """
        The value of the `scheme` attribute.

        :rtype: str
        """
        return self.__v_scheme

    @v_scheme.setter
    def v_scheme(self, v_scheme):
        self.__v_scheme = v_scheme

    @property
    def v_tag(self):
        """
        The tag of this metadatum.

        :rtype: str
        """
        return self.__v_tag

    @v_tag.setter
    def v_tag(self, v_tag):
        self.__v_tag = v_tag

    @property
    def v_text(self):
        """
        The text of this metadatum.

        :rtype: str
        """
        return self.__v_text

    @v_text.setter
    def v_text(self, v_text):
        self.__v_text = v_text

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


