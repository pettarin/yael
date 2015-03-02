#!/usr/bin/env python
# coding=utf-8

"""
A Media Overlay `<seq>` element.

Besides its own attributes,
it holds a list of `<seq>` (:class:`yael.moseq.MOSeq`)
and `<par>` (:class:`yael.mopar.MOPar`)
children elements.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.mopar import MOPar
from yael.namespace import Namespace

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.6"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class MOSeq(Element):
    """
    Build a Media Overlay `<seq>` element or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    A_TEXTREF = "textref"
    A_TYPE = "type"
    A_NS_TEXTREF = "{{{0}}}{1}".format(Namespace.EPUB, A_TEXTREF)
    A_NS_TYPE = "{{{0}}}{1}".format(Namespace.EPUB, A_TYPE)
    E_PAR = "par"
    E_SEQ = "seq"
    E_NS_PAR = "{{{0}}}{1}".format(Namespace.SMIL, E_PAR)
    E_NS_SEQ = "{{{0}}}{1}".format(Namespace.SMIL, E_SEQ)

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_epub_textref = None
        self.v_epub_type = None
        self.v_id = None
        self.children = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "epub_textref": self.v_epub_textref,
            "epub_type":    self.v_epub_type,
            "id":           self.v_id,
            "children":     len(self.children),
        }
        if recursive:
            obj["children"] = JSONAble.safe(self.children)
        return obj

    def parse_object(self, obj):
        self.v_epub_textref = obj.get(MOSeq.A_NS_TEXTREF)
        self.v_epub_type = obj.get(MOSeq.A_NS_TYPE)
        self.v_id = obj.get(MOSeq.A_ID)
        # process children
        for child in obj:
            if child.tag == MOSeq.E_NS_SEQ:
                self.add_child(MOSeq(obj=child))
            if child.tag == MOSeq.E_NS_PAR:
                self.add_child(MOPar(obj=child))

    def add_child(self, child):
        """
        Add the given child to this `<seq>`.

        :param child: the `<seq>` or `<par>` child to be added
        :type  child: :class:`yael.moseq.MOSeq` or :class:`yael.mopar.MOPar`

        """
        self.children.append(child)

    @property
    def v_epub_textref(self):
        """
        The value of the `epub:textref` attribute.

        :rtype: str
        """
        return self.__v_epub_textref

    @v_epub_textref.setter
    def v_epub_textref(self, v_epub_textref):
        self.__v_epub_textref = v_epub_textref

    @property
    def v_epub_type(self):
        """
        The value of the `epub:type` attribute.

        :rtype: str
        """
        return self.__v_epub_type

    @v_epub_type.setter
    def v_epub_type(self, v_epub_type):
        self.__v_epub_type = v_epub_type

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
    def children(self):
        """
        The list of children elements.

        :rtype: list of :class:`yael.moseq.MOSeq` and :class:`yael.mopar.MOPar`
        """
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children


