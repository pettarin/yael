#!/usr/bin/env python
# coding=utf-8

"""
An OPF `<dc:...>` metadatum.

This class can be used for both EPUB 2 and EPUB 3
DC metadata.
"""

from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.opfmetadatum import OPFMetadatum
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.5"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFDC(OPFMetadatum):
    """
    Build an OPF `<dc:...>` metadatum or
    parse it from `obj` or `string`.
    """

    A_DIR = "dir"
    A_EVENT = "event"
    A_FILE_AS = "file-as"
    A_ID = "id"
    A_LANG = "lang"
    A_ROLE = "role"
    A_SCHEME = "scheme"
    A_NS_EVENT = "{{{0}}}{1}".format(Namespace.OPF, A_EVENT)
    A_NS_FILE_AS = "{{{0}}}{1}".format(Namespace.OPF, A_FILE_AS)
    A_NS_LANG = "{{{0}}}{1}".format(Namespace.XML, A_LANG)
    A_NS_ROLE = "{{{0}}}{1}".format(Namespace.OPF, A_ROLE)
    A_NS_SCHEME = "{{{0}}}{1}".format(Namespace.OPF, A_SCHEME)

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_dir = None
        self.v_id = None
        self.v_opf_event = None
        self.v_opf_file_as = None
        self.v_opf_role = None
        self.v_opf_scheme = None
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
            "opf_event":   self.v_opf_event,
            "opf_file_as": self.v_opf_file_as,
            "opf_role":    self.v_opf_role,
            "opf_scheme":  self.v_opf_scheme,
            "tag":         self.v_tag,
            "text":        self.v_text,
            "xml_lang":    self.v_xml_lang,
            "refinements": len(self.refinements),
        }
        if recursive:
            obj["refinements"] = JSONAble.safe(self.refinements)
        return obj

    def parse_object(self, obj):
        self.v_dir = obj.get(OPFDC.A_DIR)
        self.v_id = obj.get(OPFDC.A_ID)
        self.v_opf_event = obj.get(OPFDC.A_NS_EVENT)
        self.v_opf_file_as = obj.get(OPFDC.A_NS_FILE_AS)
        self.v_opf_role = obj.get(OPFDC.A_NS_ROLE)
        self.v_opf_scheme = obj.get(OPFDC.A_NS_SCHEME)
        self.v_tag = obj.tag
        self.v_text = yael.util.safe_strip(obj.text)
        self.v_xml_lang = obj.get(OPFDC.A_NS_LANG)

    @property
    def v_dir(self):
        """
        The value of the `dir` attribute.
        EPUB 3 only.

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
    def v_opf_event(self):
        """
        The value of the `opf:event` attribute.
        EPUB 2 only.

        :rtype: str
        """
        return self.__v_opf_event

    @v_opf_event.setter
    def v_opf_event(self, v_opf_event):
        self.__v_opf_event = v_opf_event

    @property
    def v_opf_file_as(self):
        """
        The value of the `opf:file-as` attribute.
        EPUB 2 only.

        :rtype: str
        """
        return self.__v_opf_file_as

    @v_opf_file_as.setter
    def v_opf_file_as(self, v_opf_file_as):
        self.__v_opf_file_as = v_opf_file_as

    @property
    def v_opf_role(self):
        """
        The value of the `opf:role` attribute.
        EPUB 2 only.

        :rtype: str
        """
        return self.__v_opf_role

    @v_opf_role.setter
    def v_opf_role(self, v_opf_role):
        self.__v_opf_role = v_opf_role

    @property
    def v_opf_scheme(self):
        """
        The value of the `opf:scheme` attribute.
        EPUB 2 only.

        :rtype: str
        """
        return self.__v_opf_scheme

    @v_opf_scheme.setter
    def v_opf_scheme(self, v_opf_scheme):
        self.__v_opf_scheme = v_opf_scheme

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
        EPUB 3 only.

        :rtype: str
        """
        return self.__v_xml_lang

    @v_xml_lang.setter
    def v_xml_lang(self, v_xml_lang):
        self.__v_xml_lang = v_xml_lang


