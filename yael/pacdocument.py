#!/usr/bin/env python
# coding=utf-8

"""
An abstract Package Document.

At the moment, the
:class:`yael.opfpacdocument.OPFPacDocument`
is the only concrete subclass of this class.

This class is here in case future EPUB specifications
will allow different Package Document formats.
"""

from yael.element import Element

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.7"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class PacDocument(Element):
    """
    An abstract Package Document.

    You should not use this class,
    but rather its subclass
    :class:`yael.opfpacdocument.OPFPacDocument`.

    """

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_unique_identifier = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "unique_identifier": self.v_unique_identifier
        }
        return obj

    def parse_object(self, obj):
        pass

    @property
    def v_unique_identifier(self):
        """
        The Unique Identifier.

        :rtype: str
        """
        return self.__v_unique_identifier

    @v_unique_identifier.setter
    def v_unique_identifier(self, v_unique_identifier):
        self.__v_unique_identifier = v_unique_identifier

    @property
    def internal_path_cover_image(self):
        """
        The path of the cover image,
        relative to the Container root.

        :rtype: str
        """
        return None

    @property
    def internal_path_nav_document(self):
        """
        The path of the Navigation Document,
        relative to the Container root.

        :rtype: str
        """
        return None

    @property
    def internal_path_ncx_toc(self):
        """
        The path of the NCX TOC,
        relative to the Container root.

        :rtype: str
        """
        return None

    @property
    def files_referenced_manifest(self):
        """
        The (ordered) list of files referenced
        in the Package Document manifest.

        Each file is represented by its path,
        relative to the Container root.

        :rtype: list of str
        """
        return []

    #def filtered_files_referenced_manifest(self, filter_function):
    #    """
    #    The list of files referenced
    #    in the Package Document manifest.
    #    matching the given filterFunction(e),
    #    where e is a manifest item.
    #    Each file is represented by its path,
    #    relative to the Container root.
    #
    #    :param filter_function: a boolean function, taking a parameter e
    #    :type:                  function
    #    :rtype:                 list of str
    #    """
    #    return []

    @property
    def files_referenced_spine(self):
        """
        The (ordered) list of files referenced
        in the Package Document spine.

        Each file is represented by its path,
        relative to the Container root.

        :rtype: list of str
        """
        return []

    @property
    def files_referenced_spine_linear(self):
        """
        The (ordered) list of files referenced
        in the Package Document spine
        with attribute `linear="yes"` or omitted.

        Each file is represented by its path,
        relative to the Container root.

        :rtype: list of str
        """
        return []


