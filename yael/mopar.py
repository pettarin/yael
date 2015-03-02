#!/usr/bin/env python
# coding=utf-8

"""
A Media Overlay `<par>` element.

Besides its own attributes, it should have
either a `<text>` (:class:`yael.motext.MOText`) child,
or
both a `<text>` (:class:`yael.motext.MOText`)
and an `<audio>` (:class:`yael.moaudio.MOAudio`) children.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.moaudio import MOAudio
from yael.motext import MOText
from yael.namespace import Namespace

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.6"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class MOPar(Element):
    """
    Build a Media Overlay `<par>` element or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    A_TYPE = "type"
    A_NS_TYPE = "{{{0}}}{1}".format(Namespace.EPUB, A_TYPE)
    E_AUDIO = "audio"
    E_TEXT = "text"
    E_NS_AUDIO = "{{{0}}}{1}".format(Namespace.SMIL, E_AUDIO)
    E_NS_TEXT = "{{{0}}}{1}".format(Namespace.SMIL, E_TEXT)

    def __init__(self, internal_path=None, obj=None, string=None):
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
            "epub_type": self.v_epub_type,
            "id":        self.v_id,
            "children":  len(self.children),
        }
        if recursive:
            obj["children"] = JSONAble.safe(self.children)
        return obj

    def parse_object(self, obj):
        self.v_epub_type = obj.get(MOPar.A_NS_TYPE)
        self.v_id = obj.get(MOPar.A_ID)

        # process children
        for child in obj:
            if child.tag == MOPar.E_NS_TEXT:
                self.add_child(MOText(obj=child))
            if child.tag == MOPar.E_NS_AUDIO:
                self.add_child(MOAudio(obj=child))

    def add_child(self, child):
        """
        Add the given child to this `<par>`.

        :param child: the `<text>` or `<audio>` child to be added
        :type  child: :class:`yael.moaudio.MOAudio` or
                      :class:`yael.motext.MOText`

        """
        self.children.append(child)

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
        The children elements of this `<par>`.

        Note: this is implemented as a list
        (instead of two instance variables,
        one for `<audio>` and one for `<text>`)
        to accommodate a bright future when the spec will allow
        multiple children elements,
        e.g. several `<text>` for each `<audio>`.

        :rtype: list of :class:`yael.moaudio.MOAudio` and
                :class:`yael.motext.MOText`
        """
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children

    @property
    def has_audio_child(self):
        """
        True if this `<par>` has an `<audio>` child.

        :rtype: bool
        """
        lis = list(e for e in self.children if isinstance(e, MOAudio))
        return len(lis) > 0


