#!/usr/bin/env python
# coding=utf-8

"""
An asset (file) of a Publication.

The asset is identified by its `internal_path`
inside the virtual container of the publication.

The contents of the asset can be specified:

1. by storing its bytes in the `data` property
2. by specifying the `absolute_path` to a file on disk
3. by specifying the `absolute_path` (pointing to a directory on disk)
   and the corresponding `relative_path` (to a file)
4. by specifying the `absolute_path` (pointing to a ZIP file on disk)
   and the corresponding `relative_path` (the ZIP entry name)
"""

import os
import zipfile

from yael.jsonable import JSONAble
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.4"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Asset(JSONAble):
    """
    Build an asset.

    :param absolute_path: the absolute path
    :type absolute_path:  str
    :param relative_path: the relative path
    :type relative_path:  str
    :param internal_path: the internal path
    :type internal_path:  str
    :param data:          a data (bytes) object
    :type data:           bytes

    """

    def __init__(
            self,
            absolute_path=None,
            relative_path=None,
            internal_path=None,
            data=None):
        self.absolute_path = absolute_path
        self.relative_path = relative_path
        self.internal_path = internal_path
        self.data = data
        self.obfuscation_algorithm = None
        self.obfuscation_key = None

    def json_object(self, recursive=True):
        obj = {
            "absolute_path":         self.absolute_path,
            "relative_path":         self.relative_path,
            "internal_path":         self.internal_path,
            "data":                  (self.data == None),
            "obfuscation_algorithm": self.obfuscation_algorithm,
            "obfuscation_key":       self.obfuscation_key,
        }
        return obj

    @property
    def absolute_path(self):
        """
        The absolute path of the container of this asset
        (if `relative_path` is not None) or
        the absolute path of this asset
        (if `relative_path` is None).

        :rtype: str
        """
        return self.__absolute_path

    @absolute_path.setter
    def absolute_path(self, absolute_path):
        self.__absolute_path = absolute_path

    @property
    def relative_path(self):
        """
        The path of this asset,
        relative to the container root
        specified by `absolute_path`.

        :rtype: str
        """
        return self.__relative_path

    @relative_path.setter
    def relative_path(self, relative_path):
        self.__relative_path = relative_path

    @property
    def internal_path(self):
        """
        The internal path of this asset,
        relative to the virtual container root.

        :rtype: str
        """
        return self.__internal_path

    @internal_path.setter
    def internal_path(self, internal_path):
        self.__internal_path = internal_path

    @property
    def data(self):
        """
        The contents (i.e., bytes) of this asset,
        set programmatically.

        :rtype: bytes
        """
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def obfuscation_algorithm(self):
        """
        The obfuscation algorithm to be used
        or None if the asset should not be obfuscated.

        :rtype: :class:`yael.obfuscation.Obfuscation`
        """
        return self.__obfuscation_algorithm

    @obfuscation_algorithm.setter
    def obfuscation_algorithm(self, obfuscation_algorithm):
        self.__obfuscation_algorithm = obfuscation_algorithm

    @property
    def obfuscation_key(self):
        """
        The obfuscation key to be used
        or None if the asset should not be obfuscated.

        :rtype: str
        """
        return self.__obfuscation_key

    @obfuscation_key.setter
    def obfuscation_key(self, obfuscation_key):
        self.__obfuscation_key = obfuscation_key

    @property
    def contents(self):
        """
        The contents of this asset.

        The return value is obtained by either reading
        the `data` property (case 1), or by suitably
        reading the contents from the file system
        (cases 2, 3, and 4).

        If the asset is obfuscated, this function
        will run the (un)obfuscation algorithm
        on the raw_contents.

        :rtype: bytes
        """

        raw_data = self.raw_contents
        if self.obfuscation_key == None:
            return raw_data

        return yael.util.obfuscate_data(
            data=raw_data,
            key=self.obfuscation_key,
            algorithm=self.obfuscation_algorithm)

    @property
    def raw_contents(self):
        """
        The raw contents of this asset.

        The return value is obtained by either reading
        the `data` property (case 1), or by suitably
        reading the contents from the file system
        (cases 2, 3, and 4).

        :rtype: bytes
        """

        if self.data != None:
            return self.data

        try:
            if (
                    (self.absolute_path != None) and
                    (os.path.exists(self.absolute_path))):
                if (
                        (os.path.isdir(self.absolute_path)) or
                        (self.relative_path == None)):

                    if self.relative_path == None:
                        # uncompressed, abs pointing to a file
                        a_p_asset = self.absolute_path
                    else:
                        # uncompressed, abs + rel
                        a_p_asset = yael.util.norm_join(
                            self.absolute_path,
                            self.relative_path)
                    fil = open(a_p_asset, mode="rb")
                    string = fil.read()
                    fil.close()
                    return string
                else:
                    # compressed
                    zip_file = zipfile.ZipFile(self.absolute_path, mode="r")
                    string = zip_file.read(self.relative_path)
                    zip_file.close()
                    return string
        except:
            pass

        return None



