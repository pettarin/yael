#!/usr/bin/env python
# coding=utf-8

"""
An abstract OPF metadatum, that is, a child of `<metadata>`.

It has three subclasses:

1. :class:`yael.opfdc.OPFDC`
2. :class:`yael.opfmeta2.OPFMeta2`
3. :class:`yael.opfmeta3.OPFMeta3`
"""

from yael.element import Element
from yael.jsonable import JSONAble

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.2"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFMetadatum(Element):
    """
    An abstract OPF metadatum, that is, a child of `<metadata>`.

    You should not use this class,
    but rather one of its subclasses:

    1. :class:`yael.opfdc.OPFDC`
    2. :class:`yael.opfmeta2.OPFMeta2`
    3. :class:`yael.opfmeta3.OPFMeta3`

    """

    def __init__(self, internal_path=None, obj=None, string=None):
        self.refinements = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "refinements": len(self.refinements),
        }
        if recursive:
            obj["refinements"] = JSONAble.safe(self.refinements)
        return obj

    def parse_object(self, obj):
        pass

    def add_refinement(self, refinement):
        """
        Add a refinement, that is,
        store a reference to the refinement metadatum.

        :param refinement: the refinement metadatum
        :type  refinement: :class:`yael.opfmetadatum.OPFMetadatum`

        """
        self.refinements.append(refinement)



