#!/usr/bin/env python
# coding=utf-8

"""
A simplified interface
for reading, editing, and writing
EPUB 2 and EPUB 3 eBooks
with just one Rendition.

It also exposes some vanity functions.

If you need Multiple Renditions or more control,
you should use :class:`yael.publication.Publication` instead.
"""

from yael.dc import DC
from yael.navnode import NavNode
from yael.ncxtocnode import NCXTocNode
from yael.parsing import Parsing
from yael.publication import Publication
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.4"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class SimpleEPUB(object):
    """
    Build a simple EPUB programmatically or parse it from `path`.

    :param path:            a path to an EPUB (compressed) file
                            or to a directory (uncompressed)
    :type  path:            str
    :param parsing_options: a list of parsing options
    :type  parsing_options: list of :class:`yael.parsing.Parsing` values
    """

    def __init__(self, path=None, parsing_options=None):
        self.path = path
        self.parsing_options = parsing_options
        if parsing_options == None:
            self.parsing_options = [Parsing.NO_MEDIA_OVERLAY]
        self.ebook = Publication(
            path=self.path,
            parsing_options=self.parsing_options)

    def __str__(self):
        return str(self.ebook)

    @property
    def manifestation(self):

        """
        The manifestation of this Publication.

        :rtype: :class:`yael.manifestation.Manifestation`
        """
        return self.ebook.manifestation

    @property
    def version(self):
        """
        The value of the EPUB version (it should be "2.0" or "3.0").

        :rtype: str
        """
        return self.ebook.version

    @property
    def dcterms_modified(self):
        """
        The value of the dcterms:modified date. (EPUB 3)

        :rtype: str
        """
        return self.ebook.dcterms_modified

    @property
    def unique_identifier(self):
        """
        The value of the unique identifier.

        :rtype: str
        """
        return self.ebook.unique_identifier

    @property
    def release_identifier(self):
        """
        The value of the release identifier.

        :rtype: str
        """
        return self.ebook.release_identifier

    @property
    def identifier(self):
        """
        The value of the (first) dc:identifier metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_IDENTIFIER)

    @property
    def title(self):
        """
        The value of the (first) dc:title metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_TITLE)

    @property
    def language(self):
        """
        The value of the (first) dc:language metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_LANGUAGE)

    @property
    def author(self):
        """
        The value of the (first) dc:author metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_CREATOR)

    @property
    def date(self):
        """
        The value of the (first) dc:date metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_DATE)

    @property
    def description(self):
        """
        The value of the (first) dc:description metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_DESCRIPTION)

    @property
    def publisher(self):
        """
        The value of the (first) dc:publisher metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_PUBLISHER)

    @property
    def rights(self):
        """
        The value of the (first) dc:rights metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_RIGHTS)

    @property
    def source(self):
        """
        The value of the (first) dc:source metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_SOURCE)

    @property
    def subjects(self):
        """
        The list of values of dc:subject metadata.

        :rtype: list of str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_SUBJECT, only_first=False)

    @property
    def type(self):
        """
        The value of the (first) dc:type metadatum.

        :rtype: str
        """
        return self.get_dc_metadatum(tag=DC.E_NS_TYPE)

    @property
    def internal_path_cover_image(self):
        """
        The path of cover image, relative to the Container root.

        :rtype: str
        """
        return self.ebook.internal_path_cover_image

    @property
    def cover_image(self):
        """
        The contents of the cover image.

        :rtype: bytes
        """
        try:
            i_p_cover = self.internal_path_cover_image
            return self.ebook.assets[i_p_cover].contents
        except:
            pass
        return None

    @property
    def toc(self):
        """
        The TOC.

        :rtype: :class:`yael.navelement.NavElement` or
                :class:`yael.ncxtoc.NCXToc`
        """
        return self.ebook.container.default_rendition.toc

    @property
    def resolved_toc(self):
        """
        The TOC, where the src values have been resolved
        into the corresponding internal paths
        (relative to the container root).

        :rtype: :class:`yael.navelement.NavElement` or
                :class:`yael.ncxtoc.NCXToc`
        """
        resolved_toc = self.toc
        if resolved_toc != None:
            i_p_toc = resolved_toc.internal_path
            for node in resolved_toc.children:
                self._resolve_reference(i_p_toc, node)
        return resolved_toc

    @property
    def landmarks(self):
        """
        The landmarks (EPUB 3 only).

        :rtype: :class:`yael.navelement.NavElement`
        """
        return self.ebook.container.default_rendition.landmarks

    @property
    def resolved_landmarks(self):
        """
        The landmarks (EPUB 3 only),
        where the src values have been resolved
        into the corresponding internal paths
        (relative to the container root).

        :rtype: :class:`yael.navelement.NavElement`
        """
        resolved_landmarks = self.landmarks
        if resolved_landmarks != None:
            i_p_landmarks = resolved_landmarks.internal_path
            for node in resolved_landmarks.children:
                self._resolve_reference(i_p_landmarks, node)
        return resolved_landmarks

    @property
    def resolved_spine(self):
        """
        The spine, as a (ordered) list of internal paths
        to the assets referenced in the actual OPF `<spine>`.

        :rtype: list of str
        """
        return self.ebook.container.default_rendition.pac_document.files_referenced_spine

    def spine_index_by_internal_path(self, internal_path):
        """
        Return the index in the spine of the file located
        at the given internal path (relative to the Container root).

        :param internal_path: the internal path of the desired item
        :type  internal_path: str
        :returns:             the index in the spine, or -1 if not found
        :rtype:               int
        """
        return self.ebook.container.default_rendition.pac_document.spine_index_by_internal_path(internal_path)

    @property
    def resolved_spine_linear(self):
        """
        The spine, as a (ordered) list of internal paths
        to the assets referenced in the actual OPF `<spine>`,
        with attribute linear="yes" or omitted.

        :rtype: list of str
        """
        return self.ebook.container.default_rendition.pac_document.files_referenced_spine_linear

    def spine_linear_index_by_internal_path(self, internal_path):
        """
        Return the index in the linear spine of the file located
        at the given internal path (relative to the Container root).

        :param internal_path: the internal path of the desired item
        :type  internal_path: str
        :returns:             the index in the spine, or -1 if not found
        :rtype:               int
        """
        return self.ebook.container.default_rendition.pac_document.spine_linear_index_by_internal_path(internal_path)

    def _resolve_reference(self, internal_path, node):
        if (isinstance(node, NavNode)) and (node.v_href != None):
            node.v_href = yael.util.norm_join_parent(
                internal_path,
                node.v_href)
        if (isinstance(node, NCXTocNode)) and (node.v_src != None):
            node.v_src = yael.util.norm_join_parent(
                internal_path,
                node.v_src)
        for child in node.children:
            self._resolve_reference(internal_path, child)

    def get_dc_metadatum(self, tag, only_first=True, as_string=True):
        """
        Get the value(s) of `<dc:...>` metadatum/metadata.

        :param tag:        the name of the desired metadatum
                           Use a :class:`yael.dc.DC` `E_NS_` value.
        :type  tag:        str
        :param only_first: only return the first metadatum
        :type  only_first: bool
        :param as_string:  return only the value of the metadatum, as a string
        :type  as_string:  bool
        :rtype:            (list of) str or :class:`yael.opfdc.OPFDC`
        """
        metadata = self.ebook.container.default_rendition.pac_document.metadata
        titles = metadata.metadata_by_tag(tag)
        if not as_string:
            return titles
        if len(titles) > 0:
            if only_first:
                return titles[0].v_text
            else:
                accumulator = []
                for title in titles:
                    if title.v_text != None and len(title.v_text) > 0:
                        accumulator.append(title.v_text)
                return accumulator
        else:
            if only_first:
                return None
            else:
                return []

    def asset_contents(self, internal_path):
        """
        Return the contents of the asset with the given
        internal path, relative to the container root.

        :param internal_path: the internal path of the desired asset
        :type  internal_path: str
        :rtype:               bytes
        """
        try:
            return self.ebook.assets[internal_path].contents
        except:
            pass
        return None



