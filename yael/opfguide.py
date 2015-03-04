#!/usr/bin/env python
# coding=utf-8

"""
An OPF `<guide>` element.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.opfreference import OPFReference
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.9"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFGuide(Element):
    """
    Build an OPF `<guide>` element or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    E_REFERENCE = "reference"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_id = None
        self.references = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def parse_object(self, obj):
        # get attributes
        self.v_id = obj.get(OPFGuide.A_ID)

        # locate `<reference>` elements
        reference_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}",
            args=["o", OPFGuide.E_REFERENCE],
            nsp={"o": Namespace.OPF, "x": Namespace.XML},
            required=None)
        for reference in reference_arr:
            reference_parsed = None
            try:
                reference_parsed = OPFReference(obj=reference)
            except:
                pass
            if reference_parsed != None:
                self.add_reference(reference_parsed)

    def json_object(self, recursive=True):
        obj = {
            "id":         self.v_id,
            "references": len(self.references),
        }
        if recursive:
            obj["references"] = JSONAble.safe(self.references)
        return obj

    def __len__(self):
        return len(self.references)

    def add_reference(self, reference):
        """
        Add the given `<reference>` (OPFReference) to the guide.

        :param reference: the `<reference>` (OPFReference) to be added
        :type  reference: :class:`yael.opfreference.OPFReference`
        """
        self.references.append(reference)

    def reference_by_type(self, v_type):
        """
        Return the `<reference>` child with given `type`.

        :param v_type: the desired `type`
        :type  v_type: str
        :returns:      the child with given type, or None if not found
        :rtype:        :class:`yael.opfreference.OPFReference`
        """
        lis = list(e for e in self.references if e.v_type == v_type)
        return yael.util.safe_first(lis)

    def reference_by_id(self, v_id):
        """
        Return the `<reference>` child with given `id`.

        :param v_id: the desired `id`
        :type  v_id: str
        :returns:    the child with given id, or None if not found
        :rtype:      :class:`yael.opfreference.OPFReference`
        """
        lis = list(e for e in self.references if e.v_id == v_id)
        return yael.util.safe_first(lis)

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
    def references(self):
        """
        The children elements in this guide.

        :rtype: list of :class:`yael.opfreference.OPFReference` objects
        """
        return self.__references

    @references.setter
    def references(self, references):
        self.__references = references


