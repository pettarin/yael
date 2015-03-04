#!/usr/bin/env python
# coding=utf-8

"""
A `<enc:EncryptedData>` element.

Note: this class might be incomplete and/or need refactoring.
"""

from yael.element import Element
from yael.namespace import Namespace
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.9"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class EncData(Element):
    """
    Build a `<enc:EncryptedData>` element or
    parse it from `obj` or `string`.
    """

    A_ALGORITHM = "Algorithm"
    A_ID = "Id"
    A_TYPE = "Type"
    A_URI = "URI"
    E_CIPHERDATA = "CipherData"
    E_CIPHERREFERENCE = "CipherReference"
    E_ENCRYPTIONMETHOD = "EncryptionMethod"
    E_KEYINFO = "KeyInfo"
    E_RETRIEVALMETHOD = "RetrievalMethod"
    V_ENCRYPTIONMETHOD_IDPF = "http://www.idpf.org/2008/embedding"
    V_ENCRYPTIONMETHOD_ADOBE = "http://ns.adobe.com/pdf/enc#RC"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_cipher_reference_uri = None
        self.v_encryption_method_algorithm = None
        self.v_id = None
        self.v_retrieval_method_type = None
        self.v_retrieval_method_uri = None
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def json_object(self, recursive=True):
        obj = {
            "Id":                             self.v_id,
            "ds:RetrievalMethod Type":        self.v_retrieval_method_type,
            "ds:RetrievalMethod URI":         self.v_retrieval_method_uri,
            "enc:CipherReference URI":        self.v_cipher_reference_uri,
            "enc:EncryptionMethod Algorithm":
                self.v_encryption_method_algorithm,
        }
        return obj

    def parse_object(self, obj):
        try:
            self.v_id = obj.get(EncData.A_ID)

            # locate `<enc:EncryptionMethod>` element
            encryption_method_arr = yael.util.query_xpath(
                obj=obj,
                query="{0}:{1}",
                args=['c', EncData.E_ENCRYPTIONMETHOD],
                nsp={'c': Namespace.ENC},
                required=None)
            if len(encryption_method_arr) > 0:
                self.v_encryption_method_algorithm = (
                    encryption_method_arr[0].get(EncData.A_ALGORITHM))

            # locate `<ds:KeyInfo><ds:RetrievalMethod>` element
            retrieval_method_arr = yael.util.query_xpath(
                obj=obj,
                query="{0}:{1}/{0}:{2}",
                args=['d', EncData.E_KEYINFO, EncData.E_RETRIEVALMETHOD],
                nsp={'d': Namespace.DS},
                required=None)
            if len(retrieval_method_arr) > 0:
                self.v_retrieval_method_type = retrieval_method_arr[0].get(
                    EncData.A_TYPE)
                self.v_retrieval_method_uri = retrieval_method_arr[0].get(
                    EncData.A_URI)

            # locate `<enc:CipherData><enc:CipherReference>` element
            cipher_reference_arr = yael.util.query_xpath(
                obj=obj,
                query="{0}:{1}/{0}:{2}",
                args=['e', EncData.E_CIPHERDATA, EncData.E_CIPHERREFERENCE],
                nsp={'e': Namespace.ENC},
                required=None)
            if len(cipher_reference_arr) > 0:
                self.v_cipher_reference_uri = cipher_reference_arr[0].get(
                    EncData.A_URI)

        except:
            raise Exception("Error while parsing the given object")

    @property
    def v_id(self):
        """
        The value of the `Id` attribute of `<enc:EncryptedData>`.
        """
        return self.__v_id

    @v_id.setter
    def v_id(self, v_id):
        self.__v_id = v_id

    @property
    def v_retrieval_method_type(self):
        """
        The value of the `Type` attribute of `<ds:RetrievalMethod>`.

        :rtype: str
        """
        return self.__v_retrieval_method_type

    @v_retrieval_method_type.setter
    def v_retrieval_method_type(self, v_retrieval_method_type):
        self.__v_retrieval_method_type = v_retrieval_method_type

    @property
    def v_cipher_reference_uri(self):
        """
        The value of the `URI` attribute of `<enc:CipherReference>`.

        :rtype: str
        """
        return self.__v_cipher_reference_uri

    @v_cipher_reference_uri.setter
    def v_cipher_reference_uri(self, v_cipher_reference_uri):
        self.__v_cipher_reference_uri = v_cipher_reference_uri

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
    def v_retrieval_method_uri(self):
        """
        The value of the `URI` attribute of `<ds:RetrievalMethod>`.

        :rtype: str
        """
        return self.__v_retrieval_method_uri

    @v_retrieval_method_uri.setter
    def v_retrieval_method_uri(self, v_retrieval_method_uri):
        self.__v_retrieval_method_uri = v_retrieval_method_uri


