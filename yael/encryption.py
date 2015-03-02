#!/usr/bin/env python
# coding=utf-8

"""
The `META-INF/encryption.xml` file, holding
information about encrypted/obfuscated assets.
"""

from yael.jsonable import JSONAble
from yael.element import Element
from yael.encdata import EncData
from yael.enckey import EncKey
from yael.namespace import Namespace
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.6"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Encryption(Element):
    """
    Build the `META-INF/encryption.xml` file or
    parse it from `obj` or `string`.
    """

    E_ENCRYPTEDDATA = "EncryptedData"
    E_ENCRYPTEDKEY = "EncryptedKey"
    E_ENCRYPTION = "encryption"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.encrypted_datas = []
        self.encrypted_keys = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "encrypted_datas": len(self.encrypted_datas),
            "encrypted_keys":  len(self.encrypted_keys),
        }
        if recursive:
            obj["encrypted_datas"] = JSONAble.safe(self.encrypted_datas)
            obj["encrypted_keys"] = JSONAble.safe(self.encrypted_keys)
        return obj

    def parse_object(self, obj):
        try:
            # locate `<encryption>` element
            encryption_arr = yael.util.query_xpath(
                obj=obj,
                query="/{0}:{1}",
                args=['c', Encryption.E_ENCRYPTION],
                nsp={'c': Namespace.CONTAINER},
                required=Encryption.E_ENCRYPTION)
            encryption = encryption_arr[0]

            # locate `<enc:EncryptedKey>` elements
            enc_key_arr = yael.util.query_xpath(
                obj=encryption,
                query="{0}:{1}",
                args=['e', Encryption.E_ENCRYPTEDKEY],
                nsp={'e': Namespace.ENC},
                required=None)
            for enc_key in enc_key_arr:
                enc_key_parsed = None
                try:
                    enc_key_parsed = EncKey(obj=enc_key)
                    self.encrypted_keys.append(enc_key_parsed)
                except:
                    pass

            # locate `<enc:EncryptedData>` elements
            enc_data_arr = yael.util.query_xpath(
                obj=encryption,
                query="{0}:{1}",
                args=['e', Encryption.E_ENCRYPTEDDATA],
                nsp={'e': Namespace.ENC},
                required=None)
            for enc_data in enc_data_arr:
                enc_data_parsed = None
                try:
                    enc_data_parsed = EncData(obj=enc_data)
                    self.add_enc_data(enc_data_parsed)
                except:
                    pass

        except:
            raise Exception("Error while parsing the given object")

    def add_enc_data(self, enc_data):
        """
        Add the given `<enc:EncryptedData>`.

        :param item: the `<enc:EncryptedData>` to be added
        :type  item: :class:`yael.encdata.EncData`
        """
        self.encrypted_datas.append(enc_data)

    def add_enc_key(self, enc_key):
        """
        Add the given `<enc:EncryptedKey>`.

        :param item: the `<enc:EncryptedKey>` to be added
        :type  item: :class:`yael.enckey.EncKey`
        """
        self.encrypted_keys.append(enc_key)

    @property
    def encrypted_datas(self):
        """
        The `<enc:EncryptedData>` children.

        :rtype: list of :class:`yael.encdata.EncData`
        """
        return self.__encrypted_datas

    @encrypted_datas.setter
    def encrypted_datas(self, encrypted_datas):
        self.__encrypted_datas = encrypted_datas

    @property
    def encrypted_keys(self):
        """
        The `<enc:EncryptedKey>` children.

        :rtype: list of :class:`yael.enckey.EncKey`
        """
        return self.__encrypted_keys

    @encrypted_keys.setter
    def encrypted_keys(self, encrypted_keys):
        self.__encrypted_keys = encrypted_keys

    @property
    def adobe_obfuscated_assets(self):
        """
        The list of internal paths of assets
        obfuscated with the Adobe algorithm.

        :rtype: list of str
        """
        return list(e.v_cipher_reference_uri for e in self.encrypted_datas if (
            (e.v_encryption_method_algorithm == (
                EncData.V_ENCRYPTIONMETHOD_ADOBE)) and
            (e.v_cipher_reference_uri != None)))

    @property
    def idpf_obfuscated_assets(self):
        """
        The list of internal paths of assets
        obfuscated with the IDPF algorithm.

        :rtype: list of str
        """
        return list(e.v_cipher_reference_uri for e in self.encrypted_datas if (
            (e.v_encryption_method_algorithm == (
                EncData.V_ENCRYPTIONMETHOD_IDPF)) and
            (e.v_cipher_reference_uri != None)))


