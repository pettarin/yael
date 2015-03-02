#!/usr/bin/env python
# coding=utf-8

"""
The `META-INF/metadata.xml` file, holding
the publication-wise metadata
(EPUB 3).
"""

from yael.element import Element
from yael.namespace import Namespace
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.5"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Metadata(Element):
    """
    Build the `META-INF/metadata.xml` file or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    A_PROPERTY = "property"
    A_UNIQUE_IDENTIFIER = "unique-identifier"
    E_IDENTIFIER = "identifier"
    E_META = "meta"
    E_METADATA = "metadata"
    V_DCTERMS_MODIFIED = "dcterms:modified"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_dcterms_modified = None
        self.v_unique_identifier = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "internal_path":      self.internal_path,
            "unique_identifier":  self.v_unique_identifier,
            "dcterms_modified":   self.v_dcterms_modified,
            "release_dentifier":  self.v_release_identifier
        }
        return obj

    def parse_object(self, obj):
        try:
            # locate `<container>` element
            metadata_arr = yael.util.query_xpath(
                obj=obj,
                query="/{0}:{1}",
                args=['m', Metadata.E_METADATA],
                nsp={'m': Namespace.METADATA},
                required=Metadata.E_METADATA)
            metadata = metadata_arr[0]

            # get unique-identifier id
            u_i_id = metadata.get(Metadata.A_UNIQUE_IDENTIFIER)

            # locate `<rootfile>` elements
            identifier_arr = yael.util.query_xpath(
                obj=metadata,
                query="{0}:{1}",
                args=['d', Metadata.E_IDENTIFIER],
                nsp={'d': Namespace.DC},
                required=None)
            for identifier in identifier_arr:
                i_id = identifier.get(Metadata.A_ID)
                if i_id == u_i_id:
                    self.v_unique_identifier = yael.util.safe_strip(
                        identifier.text)

            # locate `<link>` optional element
            meta_arr = yael.util.query_xpath(
                obj=metadata,
                query="{0}:{1}",
                args=['m', Metadata.E_META],
                nsp={'m': Namespace.METADATA},
                required=None)
            for meta in meta_arr:
                prop = meta.get(Metadata.A_PROPERTY)
                if prop == Metadata.V_DCTERMS_MODIFIED:
                    self.v_dcterms_modified = yael.util.safe_strip(meta.text)
        except:
            raise Exception("Error while parsing the given object")

    @property
    def v_dcterms_modified(self):
        """
        The dcterms:modified value.

        :rtype: str
        """
        return self.__v_dcterms_modified

    @v_dcterms_modified.setter
    def v_dcterms_modified(self, v_dcterms_modified):
        self.__v_dcterms_modified = v_dcterms_modified

    @property
    def v_unique_identifier(self):
        """
        The unique-identifier attribute.

        :rtype: str
        """
        return self.__v_unique_identifier

    @v_unique_identifier.setter
    def v_unique_identifier(self, v_unique_identifier):
        self.__v_unique_identifier = v_unique_identifier

    @property
    def v_release_identifier(self):
        """
        The Release Identifier, that is,
        the concatenation of the Unique Identifier
        and the dcterms:modified date.

        :rtype: str
        """
        if self.v_dcterms_modified != None:
            return "%s@%s" % (
                self.v_unique_identifier,
                self.v_dcterms_modified)
        return self.v_unique_identifier




