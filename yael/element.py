#!/usr/bin/env python
# coding=utf-8

"""
A generic file/XML node element.

It can be created
by programmatically populating its instance variables,
or by parsing a string or an XML node object.

This class is "abstract",
assigning the task of implementing
the abstract function
:func:`yael.element.Element.parse_object`
to each concrete subclass,
according to the suitable element semantics.
"""

import lxml.etree

from yael.jsonable import JSONAble

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Element(JSONAble):
    """
    Build a generic file/XML element,
    or parse it from `obj` or `string`.

    :param internal_path: a string representing the path of the element
                          inside the (possibly, virtual) EPUB container
    :type  internal_path: str
    :param obj:           an XML (`lxml`) node object to be parsed to build
                          this Element
    :type  obj:           object
    :param string:        a string to be parsed to build this Element
    :type  string:        str

    """

    def __init__(self, internal_path=None, obj=None, string=None):
        self.asset = None
        self.internal_path = internal_path
        if string != None:
            self.parse_string(string)
        elif obj != None:
            self.parse_object(obj)

    def parse_string(self, string):
        """
        Build element by parsing the given string `string`.

        :param string: a string representation to be parsed
        :type  string: str

        """

        try:
            root = lxml.etree.fromstring(string)
            self.parse_object(root)
        except:
            raise Exception("Error while parsing the given string")

    def parse_object(self, obj):
        """
        Build element by parsing the given XML node.

        :param obj: an XML node to be parsed
        :type  obj: `lxml` node object

        """

        return

    @property
    def internal_path(self):
        """
        A string representing the path of the element
        inside the (possibly, virtual) EPUB Container.
        It should be None for elements not representing files
        inside the EPUB Container.

        :rtype: str
        """

        return self.__internal_path

    @internal_path.setter
    def internal_path(self, internal_path):
        self.__internal_path = internal_path

    @property
    def asset(self):
        """
        The :class:`yael.asset.Asset` associated with this element.
        """
        return self.__asset

    @asset.setter
    def asset(self, asset):
        self.__asset = asset

    @property
    def contents(self):
        """
        The contents of the associated asset.

        :rtype: bytes
        """
        if self.asset != None:
            return self.asset.contents



