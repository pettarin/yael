#!/usr/bin/env python
# coding=utf-8

"""
An OPF `<meta>` EPUB 2 metadatum, child of the `<metadata>`.
"""

from yael.jsonable import JSONAble
from yael.opfmetadatum import OPFMetadatum
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.6"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFMeta2(OPFMetadatum):
    """
    Build an OPF `<meta>` EPUB 2 metadatum or
    parse it from `obj` or `string`.
    """

    A_CONTENT = "content"
    A_ID = "id"
    A_NAME = "name"
    V_COVER = "cover"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_content = None
        self.v_id = None
        self.v_name = None
        self.v_tag = None
        self.v_text = None
        OPFMetadatum.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "content":     self.v_content,
            "id":          self.v_id,
            "name":        self.v_name,
            "tag":         self.v_tag,
            "text":        self.v_text,
            "refinements": len(self.refinements),
        }
        if recursive:
            obj["refinements"] = JSONAble.safe(self.refinements)
        return obj

    def parse_object(self, obj):
        self.v_content = obj.get(OPFMeta2.A_CONTENT)
        self.v_id = obj.get(OPFMeta2.A_ID)
        self.v_name = obj.get(OPFMeta2.A_NAME)
        self.v_tag = obj.tag
        self.v_text = yael.util.safe_strip(obj.text)

    @property
    def v_content(self):
        """
        The value of the `content` attribute.

        :rtype: str
        """
        return self.__v_content

    @v_content.setter
    def v_content(self, v_content):
        self.__v_content = v_content

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
    def v_name(self):
        """
        The value of the `name` attribute.

        :rtype: str
        """
        return self.__v_name

    @v_name.setter
    def v_name(self, v_name):
        self.__v_name = v_name

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


