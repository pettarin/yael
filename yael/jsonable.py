#!/usr/bin/env python
# coding=utf-8

"""
A generic object which
has a JSON object/string representation.

This class is "abstract",
assigning the task of implementing
the abstract function
:func:`yael.jsonable.JSONAble.json_object`
to each concrete subclass,
according to the suitable element semantics.
"""

import json

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.4"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class JSONAble(object):
    """
    A generic object which has a JSON object/string representation.
    """

    def json_object(self, recursive=True):
        """
        To be implemented in concrete subclasses.

        :param recursive: if True, append JSON sub-objects
        :type  recursive: bool
        :returns:         object that can be output as a JSON string
        :rtype:           dict

        """

        return

    def __str__(self):
        return self.json_string(pretty=True)

    def json_string(
            self,
            recursive=True,
            pretty=False,
            indent=4,
            sort=False,
            clean=False):
        """
        Format a JSON string representation of the object.

        :param recursive: if True, append JSON sub-objects
        :type  recursive: bool
        :param pretty:    if True, pretty print the string
        :type  pretty:    bool
        :param indent:    the number of spaces for each indentation level
        :type  indent:    integer
        :param sort:      if True, sort the keys
        :type  sort:      bool
        :param clean:     if True, remove None values and empty
                          lists/dictionaries
        :type  clean:     bool
        :returns:         a JSON representation of the object
        :rtype:           str

        """

        try:
            obj = self.json_object(recursive=recursive)
            if clean:
                obj = JSONAble.clean(obj)
            if pretty:
                return json.dumps(
                    obj,
                    sort_keys=sort,
                    indent=indent,
                    separators=(',', ': '))
            else:
                return json.dumps(obj)
        except:
            pass
        return "{}"

    @staticmethod
    def safe(obj):
        """
        Return a JSON-safe representation of the given object.

        If `obj` is a list, return a list whose elements
        are the safe(...) version of the original elements,
        otherwise return the result of
        :func:`yael.jsonable.JSONAble.json_object`.

        The result might be None, if `obj` is invalid.

        :param obj: the object to represent
        :type  obj: (list of) :class:`yael.jsonable.JSONAble`
        :returs:    a JSON-safe representation of the object
        :rtype:     object

        """

        if obj != None:
            try:
                if isinstance(obj, list):
                    accumulator = []
                    for obj_elem in obj:
                        accumulator.append(JSONAble.safe(obj_elem))
                    return accumulator
                else:
                    return obj.json_object()
            except:
                pass
        return None

    # TODO find a better way of doing this
    @staticmethod
    def clean(obj):
        """
        Recursively "clean" the given object by removing:

        1. None values,
        2. empty dictionaries, and
        3. empty lists.

        Note that this function works on the given object,
        altering it in place.
        Pass a copy of the original object if you
        want to avoid side effects.

        :param obj: the object to clean
        :type  obj: value, list or dict
        :returns:   a cleaned version (possibly, None) of the given object
        :rtype:     object

        """

        if isinstance(obj, dict):
            if len(obj) < 1:
                obj = None
                return obj
            for key, value in obj.items():
                if value is None:
                    del obj[key]
                elif isinstance(value, dict) or isinstance(value, list):
                    if JSONAble.clean(value) == None:
                        del obj[key]
        elif isinstance(obj, list):
            if len(obj) < 1:
                obj = None
                return obj
            tmp = []
            for value in obj:
                clean_value = JSONAble.clean(value)
                if clean_value != None:
                    tmp.append(clean_value)
            if len(tmp) == 0:
                obj = None
            else:
                obj = tmp
        return obj



