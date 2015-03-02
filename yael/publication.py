#!/usr/bin/env python
# coding=utf-8

"""
An abstract EPUB publication.

The publication can be created
by reading and parsing a compressed (ZIP/EPUB) file
or an uncompressed directory,
or built programmatically.

TODO The publication can be written
to disk as a compressed (ZIP/EPUB) file
or as an uncompressed directory.
"""

import os

from yael.asset import Asset
from yael.container import Container
from yael.encryption import Encryption
from yael.epub import EPUB
from yael.jsonable import JSONAble
from yael.manifestation import Manifestation
from yael.modocument import MODocument
from yael.mediatype import MediaType
from yael.metadata import Metadata
from yael.navdocument import NavDocument
from yael.ncxtoc import NCXToc
from yael.obfuscation import Obfuscation
from yael.opfpacdocument import OPFPacDocument
from yael.parsing import Parsing
from yael.rmdocument import RMDocument
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.7"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Publication(JSONAble):
    """
    Build a publication or parse it from a compressed file
    or uncompressed directory.

    If `path` is not `None`, build the publication
    by reading and parsing the file or directory `path`.

    Parsing options can be specified
    by providing a non-empty list for the argument `parsing_options`.
    Recognized options are listed in :class:`yael.parsing.Parsing`.
    If `parsing_options` is empty or None, full parsing will be performed.

    :param path:            The path of the file or directory to be read.
    :type path:             str
    :param parsing_options: parsing options
    :type parsing_options:  list of :class:`yael.parsing.Parsing` options

    """

    def __init__(self, path=None, parsing_options=None):
        self.parsing_options = parsing_options
        if self.parsing_options == None:
            self.parsing_options = []
        self.path = None
        self.assets = {}
        self.container = None
        self.manifestation = None
        self.metadata = None
        self.encryption = None

        if path == None:
            self.manifestation = Manifestation.MEMORY
        else:
            if os.path.exists(path):
                self.path = path
                if os.path.isdir(path):
                    self.manifestation = Manifestation.UNCOMPRESSED
                else:
                    self.manifestation = Manifestation.COMPRESSED
                self.parse()
            else:
                raise Exception(
                    "File '%s' does not exist or it cannot be read" % path)

    def json_object(self, recursive=True):
        obj = {
            "manifestation":      self.manifestation,
            "size":               self.size,
            "path":               self.path,
            "release_identifier": self.release_identifier,
            "unique_identifier":  self.unique_identifier,
        }
        if recursive:
            obj["metadata"] = JSONAble.safe(self.metadata)
            obj["container"] = JSONAble.safe(self.container)
        return obj

    @property
    def container(self):
        """
        The META-INF/container.xml object for this Publication.

        :rtype: :class:`yael.container.Container`
        """
        return self.__container

    @container.setter
    def container(self, container):
        self.__container = container

    @property
    def metadata(self):
        """
        The META-INF/metadata.xml object for this Publication.

        :rtype: :class:`yael.metadata.Metadata`
        """
        return self.__metadata

    @metadata.setter
    def metadata(self, metadata):
        self.__metadata = metadata

    @property
    def encryption(self):
        """
        The META-INF/encryption.xml object for this Publication.

        :rtype: :class:`yael.encryption.Encryption`
        """
        return self.__encryption

    @encryption.setter
    def encryption(self, encryption):
        self.__encryption = encryption

    @property
    def manifestation(self):
        """
        The manifestation of this Publication.

        :rtype: :class:`yael.manifestation.Manifestation`
        """
        return self.__manifestation

    @manifestation.setter
    def manifestation(self, manifestation):
        self.__manifestation = manifestation

    @property
    def path(self):
        """
        The path of this Publication.

        :rtype: str
        """
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def assets(self):
        """
        The dictionary of assets in this publication.
        The keys are the internal paths of the assets,
        while the values are :class:`yael.asset.Asset` objects.

        :rtype: dict of :class:`yael.asset.Asset`
        """
        return self.__assets

    @assets.setter
    def assets(self, assets):
        self.__assets = assets

    @property
    def version(self):
        """
        The EPUB version of this Publication,
        computed as the `version` attribute of
        its default rendition.

        :rtype: str
        """
        try:
            return self.container.default_rendition.pac_document.v_version
        except:
            pass
        return None

    @property
    def unique_identifier(self):
        """
        The Unique Identifier of this Publication.

        The Unique Identifier is either:

        1. defined in the `META-INF/metadata.xml`
           (EPUB 3 publications with Multiple Renditions)
        2. defined in the Package Document of the first Rendition
           (other EPUB 2 and 3 publications)

        :rtype: str
        """

        unique_identifier = None
        try:
            if self.metadata != None:
                # use unique identifier from metadata.xml
                unique_identifier = self.metadata.v_unique_identifier
            else:
                # use unique identifier from default rendition
                p_doc = self.container.default_rendition.pac_document
                unique_identifier = p_doc.v_unique_identifier
        except:
            pass
        return unique_identifier

    @property
    def dcterms_modified(self):
        """
        The last modification date/time of this Publication.

        :rtype:   str

        """

        dcterms_modified = None
        try:
            if self.metadata != None:
                # use v_dcterms_modified from metadata.xml
                dcterms_modified = self.metadata.v_dcterms_modified
                if dcterms_modified != None:
                    return dcterms_modified
            # use v_dcterms_modified from default rendition
            p_doc = self.container.default_rendition.pac_document
            dcterms_modified = p_doc.metadata.dcterms_modified
        except:
            pass
        return dcterms_modified

    @property
    def release_identifier(self):
        """
        The Release Identifier of this Publication, that is:

        1. the concatenation of the Unique Identifier
           and the modification date in `META-INF/metadata.xml`
           (EPUB 3 publications with Multiple Renditions)
        2. the concatenation of the Unique Identifier
           and the modification date of the first Rendition
           (EPUB 3 publications without Multiple Renditions)
        3. the Unique Identifier of the first Rendition
           (EPUB 2 publications)

        :rtype:   str

        """

        release_identifier = self.unique_identifier
        try:
            if self.metadata != None:
                release_identifier = self.metadata.v_release_identifier
            else:
                dcterms_modified = self.dcterms_modified
                if dcterms_modified != None:
                    release_identifier += "@" + dcterms_modified
        except:
            pass
        # the spec requires stripping spaces
        if release_identifier != None:
            release_identifier = release_identifier.replace(" ", "")
        return release_identifier

    #def list_assets(self):
    #    try:
    #        if self.manifestation == Manifestation.UNCOMPRESSED:
    #            return yael.util.list_all_files(path=self.path)
    #
    #        if self.manifestation == Manifestation.COMPRESSED:
    #            if self.zip_file_object_r == None:
    #                self.zip_file_object_r = zipfile.ZipFile(
    #                    self.path, mode="r")
    #            accumulator = []
    #            for zip_entry in self.zip_file_object_r.namelist():
    #                accumulator.append(zip_entry)
    #            self.safe_close_zip(self.zip_file_object_r)
    #            self.zip_file_object_r = None
    #            return accumulator
    #    except:
    #        pass
    #    return []

    @property
    def internal_path_cover_image(self):
        """
        The path of cover image, relative to the Container root.

        :rtype: str
        """
        try:
            pac_document = self.container.default_rendition.pac_document
            return pac_document.internal_path_cover_image
        except:
            pass
        return None

    def parse(self):
        """
        Parse the Publication.
        """

        # add mimetype
        i_p_mimetype = EPUB.INTERNAL_PATH_MIMETYPE
        mimetype_a = Asset(
            absolute_path=self.path,
            relative_path=i_p_mimetype,
            internal_path=i_p_mimetype)
        self.assets[i_p_mimetype] = mimetype_a

        # parse container.xml (requied)
        i_p_container = EPUB.INTERNAL_PATH_CONTAINER_XML
        container_a = Asset(
            absolute_path=self.path,
            relative_path=i_p_container,
            internal_path=i_p_container)
        self.container = Container(
            string=container_a.contents,
            internal_path=i_p_container)
        self.container.asset = container_a
        self.assets[i_p_container] = container_a

        # parse multiple renditions (if any)
        if (
                (Parsing.MULTIPLE_RENDITIONS in self.parsing_options) or
                (not Parsing.NO_MULTIPLE_RENDITIONS in self.parsing_options)):
            self.parse_multiple_renditions()
            # parse all renditions
            for rendition in self.container.renditions:
                self.parse_rendition(rendition)
        else:
            # parse only the first rendition
            if len(self.container.renditions) > 0:
                self.parse_rendition(self.container.renditions[0])

        # parse encryption.xml (if any)
        if (
                (Parsing.ENCRYPTION in self.parsing_options) or
                (not Parsing.NO_ENCRYPTION in self.parsing_options)):
            self.parse_encryption()

        # TODO parse: manifest.xml
        # TODO parse: rights.xml
        # TODO parse: signatures.xml

    def parse_encryption(self):
        """
        Parse `META-INF/encryption.xml`.
        """

        i_p_encryption = EPUB.INTERNAL_PATH_ENCRYPTION_XML
        encryption_a = Asset(
            absolute_path=self.path,
            relative_path=i_p_encryption,
            internal_path=i_p_encryption)
        encryption_a_contents = encryption_a.contents
        if encryption_a_contents != None:
            self.encryption = Encryption(
                string=encryption_a_contents,
                internal_path=i_p_encryption)
            self.encryption.asset = encryption_a
            self.assets[i_p_encryption] = encryption_a

            # TODO refactor this
            for i_p_asset in self.encryption.adobe_obfuscated_assets:
                if i_p_asset in self.assets:
                    obf_asset = self.assets[i_p_asset]
                    obf_asset.obfuscation_key = self.unique_identifier
                    obf_asset.obfuscation_algorithm = Obfuscation.ADOBE
            for i_p_asset in self.encryption.idpf_obfuscated_assets:
                if i_p_asset in self.assets:
                    obf_asset = self.assets[i_p_asset]
                    obf_asset.obfuscation_key = self.unique_identifier
                    obf_asset.obfuscation_algorithm = Obfuscation.IDPF

    def parse_multiple_renditions(self):
        """
        Parse `META-INF/metadata.xml` and Multiple Renditions.
        """
        # parse metadata.xml (if any)
        i_p_metadata = EPUB.INTERNAL_PATH_METADATA_XML
        metadata_a = Asset(
            absolute_path=self.path,
            relative_path=i_p_metadata,
            internal_path=i_p_metadata)
        metadata_a_contents = metadata_a.contents
        if metadata_a_contents != None:
            self.metadata = Metadata(
                string=metadata_a_contents,
                internal_path=i_p_metadata)
            self.metadata.asset = metadata_a
            self.assets[i_p_metadata] = metadata_a

        # parse rendition mapping document (if any)
        rmd = self.container.rm_document
        if rmd != None:
            i_p_rmd = rmd.internal_path
            rmd_a = Asset(
                absolute_path=self.path,
                relative_path=i_p_rmd,
                internal_path=i_p_rmd)
            rmd_a_contents = rmd_a.contents
            if rmd_a_contents != None:
                rmd = RMDocument(
                    string=rmd_a_contents,
                    internal_path=i_p_rmd)
                rmd.asset = rmd_a
                self.container.rm_document = rmd
                self.assets[i_p_rmd] = rmd_a

    def parse_rendition(self, rendition):
        """
        Parse the given Rendition object.
        """
        if rendition.v_media_type == MediaType.OPF:
            # parse OPF
            i_p_opf = rendition.v_full_path
            opf_a = Asset(
                absolute_path=self.path,
                relative_path=i_p_opf,
                internal_path=i_p_opf)
            opf = OPFPacDocument(string=opf_a.contents, internal_path=i_p_opf)
            opf.asset = opf_a
            self.assets[i_p_opf] = opf_a
            rendition.pac_document = opf

            # add one asset for each manifest item
            if (
                    (Parsing.ASSET_REFS in self.parsing_options) or
                    (not Parsing.NO_ASSET_REFS in self.parsing_options)):
                for item in opf.manifest.items:
                    i_p_item = yael.util.norm_join_parent(i_p_opf, item.v_href)
                    asset = Asset(
                        absolute_path=self.path,
                        relative_path=i_p_item,
                        internal_path=i_p_item)
                    item.asset = asset
                    self.assets[i_p_item] = asset

            # parse Navigation Document
            if (
                    (Parsing.NAV in self.parsing_options) or
                    (not Parsing.NO_NAV in self.parsing_options)):
                i_p_nav = opf.internal_path_nav_document
                if i_p_nav != None:
                    nav_a = Asset(
                        absolute_path=self.path,
                        relative_path=i_p_nav,
                        internal_path=i_p_nav)
                    nav = NavDocument(
                        string=nav_a.contents,
                        internal_path=i_p_nav)
                    nav.asset = nav_a
                    self.assets[i_p_nav] = nav_a
                    rendition.nav_document = nav

            # parse NCX
            if (
                    (Parsing.NCX in self.parsing_options) or
                    (not Parsing.NO_NCX in self.parsing_options)):
                i_p_ncx = opf.internal_path_ncx_toc
                if i_p_ncx != None:
                    ncx_a = Asset(
                        absolute_path=self.path,
                        relative_path=i_p_ncx,
                        internal_path=i_p_ncx)
                    ncx = NCXToc(
                        string=ncx_a.contents,
                        internal_path=i_p_ncx)
                    ncx.asset = ncx_a
                    self.assets[i_p_ncx] = ncx_a
                    rendition.ncx_toc = ncx

            # parse Media Overlay Documents
            if (
                    (Parsing.MEDIA_OVERLAY in self.parsing_options) or
                    (not Parsing.NO_MEDIA_OVERLAY in self.parsing_options)):
                for smil_item in opf.manifest.mo_document_items:
                    smil_item_parsed = None
                    try:
                        i_p_smil = yael.util.norm_join_parent(
                            i_p_opf,
                            smil_item.v_href)
                        smil_a = Asset(
                            absolute_path=self.path,
                            relative_path=i_p_smil,
                            internal_path=i_p_smil)
                        smil_item_parsed = MODocument(
                            string=smil_a.contents,
                            internal_path=i_p_smil)
                        smil_item_parsed.asset = smil_a
                        self.assets[i_p_smil] = smil_a
                    except:
                        pass
                    if smil_item_parsed != None:
                        rendition.add_mo_document(smil_item_parsed)

    @property
    def size(self):
        """
        Compute and return the size of the publication.

        For a :const:`yael.manifestation.Manifestation.COMPRESSED`
        publication, it is the size of the EPUB (ZIP) Container, in bytes.
        For a :const:`yael.manifestation.Manifestation.UNCOMPRESSED`
        publication, it is the sum of the sizes, in bytes, of the files
        in the uncompressed directory.
        In all other cases (i.e.,
        for a :const:`yael.manifestation.Manifestation.MEMORY`
        publication), returns -1.

        :rtype:   int

        """

        if self.manifestation == Manifestation.COMPRESSED:
            return os.path.getsize(self.path)

        if self.manifestation == Manifestation.UNCOMPRESSED:
            return yael.util.directory_size(self.path)

        # TODO perhaps some sort of memory footprint size might be useful
        return -1


