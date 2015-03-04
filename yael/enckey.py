#!/usr/bin/env python
# coding=utf-8

"""
A `<enc:EncryptedKey>` element.

Note: this class might be incomplete and/or need refactoring.
"""

from yael.element import Element
from yael.namespace import Namespace
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.8"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class EncKey(Element):
    """
    Build a `<enc:EncryptedKey>` element or
    parse it from `obj` or `string`.
    """

    A_ALGORITHM = "Algorithm"
    A_ID = "Id"
    A_URI = "URI"
    E_CIPHERDATA = "CipherData"
    E_CIPHERVALUE = "CipherValue"
    E_ENCRYPTIONMETHOD = "EncryptionMethod"
    E_KEYINFO = "KeyInfo"
    E_KEYNAME = "KeyName"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_cipher_value = None
        self.v_encryption_method_algorithm = None
        self.v_id = None
        self.v_key_name = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "Id":                             self.v_id,
            "ds:KeyName":                     self.v_key_name,
            "enc:CipherValue":                self.v_cipher_value,
            "enc:EncryptionMethod Algorithm":
                self.v_encryption_method_algorithm,
        }
        return obj

    def parse_object(self, obj):
        try:
            self.v_id = obj.get(EncKey.A_ID)

            # locate `<enc:EncryptionMethod>` element
            encryption_method_arr = yael.util.query_xpath(
                obj=obj,
                query="{0}:{1}",
                args=['c', EncKey.E_ENCRYPTIONMETHOD],
                nsp={'c': Namespace.ENC},
                required=None)
            if len(encryption_method_arr) > 0:
                self.v_encryption_method_algorithm = (
                    encryption_method_arr[0].get(EncKey.A_ALGORITHM))

            # locate `<ds:KeyInfo><ds:KeyName>` element
            key_name_arr = yael.util.query_xpath(
                obj=obj,
                query="{0}:{1}/{0}:{2}",
                args=['d', EncKey.E_KEYINFO, EncKey.E_KEYNAME],
                nsp={'d': Namespace.DS},
                required=None)
            if len(key_name_arr) > 0:
                self.v_key_name = key_name_arr[0].text

            # locate `<enc:CipherData><enc:CipherValue>` element
            cipher_value_arr = yael.util.query_xpath(
                obj=obj,
                query="{0}:{1}/{0}:{2}",
                args=['e', EncKey.E_CIPHERDATA, EncKey.E_CIPHERVALUE],
                nsp={'e': Namespace.ENC},
                required=None)
            if len(cipher_value_arr) > 0:
                self.v_cipher_value = cipher_value_arr[0].text

        except:
            raise Exception("Error while parsing the given object")

    @property
    def v_id(self):
        """
        The value of the `Id` attribute of `<enc:EncryptedKey>`.

        :rtype: str
        """
        return self.__v_id

    @v_id.setter
    def v_id(self, v_id):
        self.__v_id = v_id

    @property
    def v_cipher_value(self):
        """
        The value of the `<enc:CipherValue>`.

        :rtype: str
        """
        return self.__v_cipher_value

    @v_cipher_value.setter
    def v_cipher_value(self, v_cipher_value):
        self.__v_cipher_value = v_cipher_value

    @property
    def v_encryption_method_algorithm(self):
        """
        The value of the `Algorithm` attribute of `<enc:EncryptionMethod>`.

        :rtype: str
        """
        return self.__v_encryption_method_algorithm

    @v_encryption_method_algorithm.setter
    def v_encryption_method_algorithm(self, v_encryption_method_algorithm):
        self.__v_encryption_method_algorithm = v_encryption_method_algorithm

    @property
    def v_key_name(self):
        """
        The value of the `<ds:KeyName>`.

        :rtype: str
        """
        return self.__v_key_name

    @v_key_name.setter
    def v_key_name(self, v_key_name):
        self.__v_key_name = v_key_name


