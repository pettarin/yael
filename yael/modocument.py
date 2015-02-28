#!/usr/bin/env python
# coding=utf-8

"""
A Media Overlay Document (SMIL file).
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.moaudio import MOAudio
from yael.mopar import MOPar
from yael.moseq import MOSeq
from yael.motext import MOText
from yael.namespace import Namespace
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.4"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class MODocument(Element):
    """
    Build a Media Overlay Document (SMIL file) or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    A_PREFIX = "prefix"
    A_VERSION = "version"
    A_NS_PREFIX = "{{{0}}}{1}".format(Namespace.EPUB, A_PREFIX)
    E_BODY = "body"
    E_HEAD = "head"
    E_SMIL = "smil"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_epub_prefix = None
        self.v_id = None
        self.v_version = None
        self.head = None # TODO currently not parsed
        self.body = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "epub_prefix": self.v_epub_prefix,
            "id":          self.v_id,
            "version":     self.v_version,
        }
        if recursive:
            obj["head"] = JSONAble.safe(self.head)
            obj["body"] = JSONAble.safe(self.body)
        return obj

    def parse_object(self, obj):
        smil_arr = yael.util.query_xpath(
            obj=obj,
            query="/{0}:{1}",
            args=["s", MODocument.E_SMIL],
            nsp={"s": Namespace.SMIL, "e": Namespace.EPUB},
            required=MODocument.E_SMIL)
        smil = smil_arr[0]

        self.v_id = smil.get(MODocument.A_ID)
        self.v_epub_prefix = smil.get(MODocument.A_NS_PREFIX)
        self.v_version = smil.get(MODocument.A_VERSION)

        # locate `<head>` element
        #head_arr = yael.util.query_xpath(
        #            obj=smil,
        #            query="{0}:{1}",
        #            args=["s", MODocument.E_HEAD],
        #            nsp={"s": Namespace.SMIL, "e": Namespace.EPUB},
        #            required=None)
        #if (len(head_arr) > 0):
        #    self.head = ...

        # locate `<body>` element
        body_arr = yael.util.query_xpath(
            obj=smil,
            query="{0}:{1}",
            args=["s", MODocument.E_BODY],
            nsp={"s": Namespace.SMIL, "e": Namespace.EPUB},
            required=MODocument.E_BODY)
        self.body = MOSeq(obj=body_arr[0])

    @property
    def v_epub_prefix(self):
        """
        The `epub:prefix` attribute of the `<smil>` element.

        :rtype: str
        """
        return self.__v_epub_prefix

    @v_epub_prefix.setter
    def v_epub_prefix(self, v_epub_prefix):
        self.__v_epub_prefix = v_epub_prefix

    @property
    def v_id(self):
        """
        The `id` attribute of the `<smil>` element.

        :rtype: str
        """
        return self.__v_id

    @v_id.setter
    def v_id(self, v_id):
        self.__v_id = v_id

    @property
    def v_version(self):
        """
        The `version` attribute of the `<smil>` element.

        :rtype: str
        """
        return self.__v_version

    @v_version.setter
    def v_version(self, v_version):
        self.__v_version = v_version

    @property
    def body(self):
        """
        The `body` child of the `<smil>` element.

        :rtype: :class:`yael.moseq.MOSeq`
        """
        return self.__body

    @body.setter
    def body(self, body):
        self.__body = body

    @property
    def head(self):
        """
        The `head` child of the `<smil>` element.

        Currently not parsed, as per specs, it is empty.

        :rtype: None
        """
        return self.__head

    @head.setter
    def head(self, head):
        self.__head = head

    @property
    def references_embedded_audio_video(self):
        """
        True if this Media Overlay Document
        references Embedded Audio and Video
        (i.e., if it contains a `<par>`
        with a `<text>` child but no `<audio>` child).

        :rtype: bool
        """

        try:
            return self._references_embedded_audio_video(self.body.children)
        except:
            pass
        return False

    @property
    def referenced_audio_files(self):
        """
        The list of audio files referenced
        by `<audio>` elements in this Media Overlay Document.

        :rtype: list of str
        """

        try:
            return list(self._referenced_audio_files(self.body.children, {}))
        except:
            pass
        return []

    @property
    def referenced_fragment_identifiers(self):
        """
        The list of fragment identifiers referenced
        by `<text>` elements in this Media Overlay Document.

        :rtype: list of str
        """

        try:
            return self._referenced_fragment_identifiers(self.body.children, [])
        except:
            pass
        return []

    @property
    def grouped_referenced_fragment_identifiers(self):
        """
        A dictionary containing the fragment identifiers referenced
        by `<text>` elements in this Media Overlay Document.
        Each key is the path to the Content Document,
        and the corresponding value is a list of fragment indentifiers
        in that Content Document.

        :rtype: dict
        """

        try:
            fis = self._referenced_fragment_identifiers(self.body.children, [])
            grouped = {}
            for fid in fis:
                dic = yael.util.split_reference(fid)
                if ("base" in dic) and ("fragment" in dic):
                    base = dic["base"]
                    fragment = dic["fragment"]
                    if base not in grouped:
                        grouped[base] = []
                    grouped[base].append(fragment)
            return grouped
        except:
            pass
        return {}

    def _references_embedded_audio_video(self, elements):
        for element in elements:
            has_embedded = False
            if isinstance(element, MOSeq):
                has_embedded = self._references_embedded_audio_video(
                    element.children)
            elif isinstance(element, MOPar):
                has_embedded = not element.has_audio_child
            if has_embedded:
                return True
        return False

    def _referenced_audio_files(self, elements, dictionary):
        for element in elements:
            if isinstance(element, MOSeq) or isinstance(element, MOPar):
                self._referenced_audio_files(element.children, dictionary)
            elif isinstance(element, MOAudio):
                path = element.v_src
                if self.internal_path != None:
                    path = yael.util.norm_join_parent(self.internal_path, path)
                dictionary[path] = True
        return dictionary

    def _referenced_fragment_identifiers(self, elements, accumulator):
        for element in elements:
            if isinstance(element, MOSeq) or isinstance(element, MOPar):
                self._referenced_fragment_identifiers(
                    element.children,
                    accumulator)
            elif isinstance(element, MOText):
                path = element.v_src
                if self.internal_path != None:
                    path = yael.util.norm_join_parent(self.internal_path, path)
                accumulator.append(path)
        return accumulator



