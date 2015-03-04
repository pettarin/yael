#!/usr/bin/env python
# coding=utf-8

"""
The OPF Package Document.
"""

from yael.jsonable import JSONAble
from yael.namespace import Namespace
from yael.opfguide import OPFGuide
from yael.opfmanifest import OPFManifest
from yael.opfmeta3 import OPFMeta3
from yael.opfmetadata import OPFMetadata
from yael.opfspine import OPFSpine
from yael.pacdocument import PacDocument
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.8"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFPacDocument(PacDocument):
    """
    Build the OPF Package Document or
    parse it from `obj` or `string`.
    """

    A_DIR = "dir"
    A_ID = "id"
    A_LANG = "lang"
    A_PREFIX = "prefix"
    A_UNIQUE_IDENTIFIER = "unique-identifier"
    A_VERSION = "version"
    A_NS_LANG = "{{{0}}}{1}".format(Namespace.XML, A_LANG)
    E_BINDINGS = "bindings"
    E_COLLECTION = "collection"
    E_GUIDE = "guide"
    E_MANIFEST = "manifest"
    E_METADATA = "metadata"
    E_PACKAGE = "package"
    E_SPINE = "spine"

    def __init__(self, internal_path=None, obj=None, string=None):
        # self.unique_identifier
        # is already defined
        # in the PacDocument class
        self.v_dir = None
        self.v_id = None
        self.v_prefix = None
        self.v_version = None
        self.v_xml_lang = None
        self.metadata = None
        self.manifest = None
        self.spine = None
        self.guide = None
        self.bindings = None # TODO currently not parsed
        self.collection = None # TODO currently not parsed
        PacDocument.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        opf = {
            "dir":               self.v_dir,
            "id":                self.v_id,
            "prefix":            self.v_prefix,
            "unique_identifier": self.v_unique_identifier,
            "version":           self.v_version,
            "xml_lang":          self.v_xml_lang,
            "metadata":          (self.metadata == None),
            "manifest":          (self.manifest == None),
            "spine":             (self.spine == None),
            "guide":             (self.guide == None),
            "bindings":          (self.bindings == None),
            "collection":        (self.collection == None),
        }
        if recursive:
            opf["metadata"] = JSONAble.safe(self.metadata)
            opf["manifest"] = JSONAble.safe(self.manifest)
            opf["spine"] = JSONAble.safe(self.spine)
            opf["guide"] = JSONAble.safe(self.guide)
            opf["bindings"] = None
            opf["collection"] = None
        return opf

    def parse_object(self, obj):
        package_arr = yael.util.query_xpath(
            obj=obj,
            query="/{0}:{1}",
            args=["o", OPFPacDocument.E_PACKAGE],
            nsp={"o": Namespace.OPF, "x": Namespace.XML},
            required=OPFPacDocument.E_PACKAGE)
        package = package_arr[0]

        self.v_id = package.get(OPFPacDocument.A_ID)
        self.v_dir = package.get(OPFPacDocument.A_DIR)
        self.v_xml_lang = package.get(OPFPacDocument.A_NS_LANG)
        self.v_prefix = package.get(OPFPacDocument.A_PREFIX)
        self.v_version = package.get(OPFPacDocument.A_VERSION)

        # locate `<manifest>` element
        manifest_arr = yael.util.query_xpath(
            obj=package,
            query="{0}:{1}",
            args=["o", OPFPacDocument.E_MANIFEST],
            nsp={"o": Namespace.OPF, 'x': Namespace.XML},
            required=OPFPacDocument.E_MANIFEST)
        self.manifest = OPFManifest(
            obj=manifest_arr[0],
            internal_path=self.internal_path)

        #locate `<metadata>` element
        metadata_arr = yael.util.query_xpath(
            obj=package,
            query="{0}:{1}",
            args=["o", OPFPacDocument.E_METADATA],
            nsp={"o": Namespace.OPF, "x": Namespace.XML},
            required=OPFPacDocument.E_METADATA)
        self.metadata = OPFMetadata(
            obj=metadata_arr[0],
            internal_path=self.internal_path)

        # locate `<spine>` element
        spine_arr = yael.util.query_xpath(
            obj=package,
            query="{0}:{1}",
            args=["o", OPFPacDocument.E_SPINE],
            nsp={"o": Namespace.OPF, "x": Namespace.XML},
            required=OPFPacDocument.E_SPINE)
        self.spine = OPFSpine(
            obj=spine_arr[0],
            internal_path=self.internal_path)

        # locate `<guide>` element
        guide_arr = yael.util.query_xpath(
            obj=package,
            query="{0}:{1}",
            args=["o", OPFPacDocument.E_GUIDE],
            nsp={"o": Namespace.OPF, "x": Namespace.XML},
            required=None)
        if len(guide_arr) > 0:
            self.guide = OPFGuide(
                obj=guide_arr[0],
                internal_path=self.internal_path)

        # set unique identifier
        u_i_id = package.get(OPFPacDocument.A_UNIQUE_IDENTIFIER)
        try:
            self.v_unique_identifier = self.metadata.metadatum_by_id(
                u_i_id).v_text
        except:
            pass

        # resolve refinements
        for metadatum in self.metadata.metadata:
            if isinstance(metadatum, OPFMeta3):
                self._resolve_refinement(metadatum)
        for link in self.metadata.links:
            self._resolve_refinement(link)

    def _resolve_refinement(self, metadatum):
        try:
            if metadatum.v_refines[0] == "#":
                refines_id = metadatum.v_refines[1:]
                # refining another metadatum?
                refined = self.metadata.metadatum_by_id(refines_id)
                if refined != None:
                    refined.add_refinement(metadatum)
                    return
                # refining a manifest item?
                refined = self.manifest.item_by_id(refines_id)
                if refined != None:
                    refined.add_refinement(metadatum)
        except:
            pass

    @property
    def relative_path_cover_image(self):
        """
        The path of the cover image, relative to this Package Document.

        :rtype: str
        """

        # EPUB 3
        try:
            href = self.manifest.cover_image_item.v_href
            if href != None:
                return href
        except:
            pass

        # EPUB 2
        try:
            cover_id = self.metadata.cover_image_item_id
            href = self.manifest.item_by_id(cover_id).v_href
            if href != None:
                return href
        except:
            pass

        # not found
        return None

    @property
    def internal_path_cover_image(self):
        """
        The path of the cover image,
        relative to the Container root.

        :rtype: str
        """

        return self.relative_to_internal(self.relative_path_cover_image)

    @property
    def relative_path_nav_document(self):
        """
        The path of the Navigation Document,
        relative to this Package Document.

        :rtype: str
        """

        try:
            return self.manifest.nav_document_item.v_href
        except:
            pass
        return None

    @property
    def internal_path_nav_document(self):
        """
        The path of the Navigation Document,
        relative to the Container root.

        :rtype: str
        """

        return self.relative_to_internal(
            self.relative_path_nav_document)

    @property
    def relative_path_ncx_toc(self):
        """
        The path of the NCX TOC,
        relative to this Package Document.

        :rtype: str
        """

        try:
            ncx_id = self.spine.v_toc
            href = self.manifest.item_by_id(ncx_id).v_href
            if href != None:
                return href
        except:
            pass
        return None

    @property
    def internal_path_ncx_toc(self):
        """
        The path of the NCX TOC,
        relative to the Container root.

        :rtype: str
        """

        return self.relative_to_internal(self.relative_path_ncx_toc)

    def relative_to_internal(self, path):
        """
        Resolve the given path (relative to this Package Document),
        into an internal path (relative to the Container root).

        :param path: the relative path (relative to OPF)
        :type  path: str
        :returns:    the internal path (relative to Container root)
        :rtype:      str

        """

        return yael.util.norm_join_parent(self.internal_path, path)

    @property
    def files_referenced_manifest(self):
        """
        The (ordered) list of files
        referenced in the OPF `<manifest>`.

        Each file is represented by its path,
        relative to the Container root.

        :rtype: list of str
        """

        #return self.filtered_files_referenced_manifest(filter_function=None)
        try:
            accumulator = []
            for item in self.manifest.items:
                path = item.v_href
                if self.internal_path != None:
                    path = self.relative_to_internal(path)
                accumulator.append(path)
            return accumulator
        except:
            pass
        return []

    #def filtered_files_referenced_manifest(self, filter_function):
    #    """
    #    The list of files referenced in the OPF <manifest>
    #    matching the given filterFunction(e), where e is a OPFItem.
    #    Each file is represented by its path,
    #    relative to the Container root.
    #
    #    :rtype: list of str
    #    """
    #
    #    try:
    #        accumulator = []
    #        items = self.manifest.items
    #        if filter_function != None:
    #            items = list(e for e in items if filter_function(e))
    #        for item in items:
    #            path = item.v_href
    #            if self.internal_path != None:
    #                path = self.relative_to_internal(path)
    #            accumulator.append(path)
    #        return accumulator
    #    except:
    #        pass
    #    return []

    @property
    def files_referenced_spine(self):
        """
        The (ordered) list of files
        referenced in the OPF `<spine>`.

        Each file is represented by its path,
        relative to the Container root.

        :rtype: list of str
        """
        try:
            return self._files_referenced_spine(self.spine.itemrefs)
        except:
            pass
        return []

    @property
    def files_referenced_spine_linear(self):
        """
        The (ordered) list of files
        referenced in the OPF <spine>
        with attribute linear="yes" or omitted.

        Each file is represented by its path,
        relative to the Container root.

        :rtype: list of str
        """

        try:
            return self._files_referenced_spine(self.spine.linear_itemrefs)
        except:
            pass
        return []

    def _files_referenced_spine(self, itemrefs):
        try:
            accumulator = []
            for itemref in itemrefs:
                idref = itemref.v_idref
                item = self.manifest.item_by_id(idref)
                if item != None:
                    path = item.v_href
                    if self.internal_path != None:
                        path = self.relative_to_internal(path)
                    accumulator.append(path)
            return accumulator
        except:
            pass
        return []

    def item_by_internal_path(self, internal_path):
        """
        Return the `<item>` child with href corresponding
        to the given internal path.

        :param internal_path: the internal path of the desired item
        :type  internal_path: str
        :returns:             the child with given path, or None if not found
        :rtype:               :class:`yael.opfitem.OPFItem`
        """
        if self.manifest != None:
            return self.manifest.item_by_internal_path(internal_path)
        return None

    def spine_index_by_internal_path(self, internal_path):
        """
        Return the index in the spine of the file located
        at the given internal path (relative to the Container root).

        :param internal_path: the internal path of the desired item
        :type  internal_path: str
        :returns:             the index in the spine, or -1 if not found
        :rtype:               int
        """

        item = self.item_by_internal_path(internal_path)
        if item != None:
            return self.spine.index_by_idref(item.v_id)
        return -1

    def spine_linear_index_by_internal_path(self, internal_path):
        """
        Return the index in the linear spine of the file located
        at the given internal path (relative to the Container root).

        :param internal_path: the internal path of the desired item
        :type  internal_path: str
        :returns:             the index in the spine, or -1 if not found
        :rtype:               int
        """

        item = self.item_by_internal_path(internal_path)
        if item != None:
            return self.spine.linear_index_by_idref(item.v_id)
        return -1

    @property
    def v_dir(self):
        """
        The value of the `dir` attribute.

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
    def v_prefix(self):
        """
        The value of the `prefix` attribute.

        :rtype: str
        """
        return self.__v_prefix

    @v_prefix.setter
    def v_prefix(self, v_prefix):
        self.__v_prefix = v_prefix

    @property
    def v_version(self):
        """
        The value of the `version` attribute.

        :rtype: str
        """
        return self.__v_version

    @v_version.setter
    def v_version(self, v_version):
        self.__v_version = v_version

    @property
    def v_xml_lang(self):
        """
        The value of the `xml:lang` attribute.

        :rtype: str
        """
        return self.__v_xml_lang

    @v_xml_lang.setter
    def v_xml_lang(self, v_xml_lang):
        self.__v_xml_lang = v_xml_lang

    @property
    def metadata(self):
        """
        The list of metadatum objects.

        :rtype: :class:`yael.opfmetadata.OPFMetadata`
        """
        return self.__metadata

    @metadata.setter
    def metadata(self, metadata):
        self.__metadata = metadata

    @property
    def manifest(self):
        """
        The list of manifest item objects.

        :rtype: :class:`yael.opfmanifest.OPFManifest`
        """
        return self.__manifest

    @manifest.setter
    def manifest(self, manifest):
        self.__manifest = manifest

    @property
    def spine(self):
        """
        The list of spine itemref objects.

        :rtype: :class:`yael.opfspine.OPFSpine`
        """
        return self.__spine

    @spine.setter
    def spine(self, spine):
        self.__spine = spine

    @property
    def guide(self):
        """
        The list of guide references objects.

        :rtype: :class:`yael.opfguide.OPFGuide`
        """
        return self.__guide

    @guide.setter
    def guide(self, guide):
        self.__guide = guide

    @property
    def bindings(self):
        """
        Currently not parsed.

        :rtype: None
        """
        return self.__bindings

    @bindings.setter
    def bindings(self, bindings):
        self.__bindings = bindings

    @property
    def collection(self):
        """
        Currently not parsed.

        :rtype: None
        """
        return self.__collection

    @collection.setter
    def collection(self, collection):
        self.__collection = collection


