#!/usr/bin/env python
# coding=utf-8

"""
A Media Overlay `<audio>` element.
"""

from yael.element import Element
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.4"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class MOAudio(Element):
    """
    Build a Media Overlay `<audio>` element or
    parse it from `obj` or `string`.
    """

    A_CLIPBEGIN = "clipBegin"
    A_CLIPEND = "clipEnd"
    A_ID = "id"
    A_SRC = "src"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_clip_begin = None
        self.v_clip_end = None
        self.v_id = None
        self.v_src = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "clip_begin":         self.v_clip_begin,
            "clip_begin_seconds": self.clip_begin_seconds,
            "clip_end":           self.v_clip_end,
            "clip_end_seconds":   self.clip_end_seconds,
            "id":                 self.v_id,
            "src":                self.v_src,
        }
        return obj

    def parse_object(self, obj):
        self.v_clip_begin = obj.get(MOAudio.A_CLIPBEGIN)
        self.v_clip_end = obj.get(MOAudio.A_CLIPEND)
        self.v_id = obj.get(MOAudio.A_ID)
        self.v_src = obj.get(MOAudio.A_SRC)

    @property
    def clip_begin_seconds(self):
        """
        The value of the `clipBegin` attribute, in seconds.
        If `clipBegin` is None, return 0.

        :rtype: float
        """
        if self.v_clip_begin == None:
            return 0
        return yael.util.clip_time_seconds(self.v_clip_begin)

    @property
    def clip_end_seconds(self):
        """
        The value of the `clipEnd` attribute, in seconds.
        If `clipEnd` is None, return -1.

        :rtype: float
        """
        if self.v_clip_end == None:
            return -1
        return yael.util.clip_time_seconds(self.v_clip_end)

    @property
    def v_clip_begin(self):
        """
        The value of the `clipBegin` attribute.

        :rtype: str
        """
        return self.__v_clip_begin

    @v_clip_begin.setter
    def v_clip_begin(self, v_clip_begin):
        self.__v_clip_begin = v_clip_begin

    @property
    def v_clip_end(self):
        """
        The value of the `clipEnd` attribute.

        :rtype: str
        """
        return self.__v_clip_end

    @v_clip_end.setter
    def v_clip_end(self, v_clip_end):
        self.__v_clip_end = v_clip_end

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
    def v_src(self):
        """
        The value of the `src` attribute.

        :rtype: str
        """
        return self.__v_src

    @v_src.setter
    def v_src(self, v_src):
        self.__v_src = v_src



