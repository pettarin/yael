#!/usr/bin/env python
# coding=utf-8

"""
Common utility (static) functions.
"""

import hashlib
import os
import re

from yael.obfuscation import Obfuscation

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.7"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

#: pattern to match viewport value `width=W, height=H`
VP_PATTERN_WH = re.compile(r"^width[ ]*=[ ]*([0-9\.]*)[ px]*,[ ]*height[ ]*=[ ]*([0-9\.]*)[ px]*$")

#: pattern to match viewport value `height=H, width=W`
VP_PATTERN_HW = re.compile(r"^height[ ]*=[ ]*([0-9\.]*)[ px]*,[ ]*width[ ]*=[ ]*([0-9\.]*)[ px]*$")

def directory_size(path):
    """
    Compute the total size, in bytes,
    of all the files in the filesystem tree
    rooted at the given directory.

    :param path: the path of the root directory
    :type  path: str
    :returns:    the total size in bytes of the subtree rooted at `path`
    :type:       integer

    """

    total = 0
    for dir_path, unused_dir_names, file_names in os.walk(path):
        for file_name in file_names:
            total += os.path.getsize(os.path.join(dir_path, file_name))
    return total

def list_all_files(path):
    """
    List all files in the filesystem tree
    rooted at the given directory.

    :param path: the path to the root directory
    :type  path: str
    :returns:    the list of files in the subtree rooted at `path`
    :type:       list of str
    """

    accumulator = []
    if (path != None) and (os.path.exists(path)) and (os.path.isdir(path)):
        for dir_path, unused_dir_names, file_names in os.walk(path):
            for file_name in file_names:
                accumulator.append(os.path.join(dir_path, file_name))
    return accumulator

def norm_join(path1, path2):
    """
    Join the two given paths and normalize the result.

    :param path1: prefix path
    :type  path1: str
    :param path2: suffix path
    :type  path2: str
    :returns:     the join of the two paths, normalized
    :rtype:       str

    """

    if (path1 == None) or (path2 == None):
        return None
    return os.path.normpath(os.path.join(path1, path2))

def norm_join_parent(path1, path2):
    """
    Join the parent directory of path1 with path2 and normalize the result.

    :param path1: prefix path
    :type  path1: str
    :param path2: suffix path
    :type  path2: str
    :returns:     the join of the parent directory of path1 with path2,
                  and normalize (e.g., "a/../b/c" => "b/c") the result
    :rtype:       str

    """

    if (path1 == None) or (path2 == None):
        return None
    return norm_join(os.path.dirname(path1), path2)


def safe_strip(string):
    """
    Strip the given string, dealing safely with None arguments.

    :param string: the string to be stripped
    :type  string: str
    :returns:      the stripped string (or None if string is None)
    :rtype:        str

    """

    if string != None:
        string = string.strip()
    return string


def safe_first(lis):
    """
    Return the first element of the list,
    dealing safely with None or empty arguments.

    :param lis: a list of objects or values
    :type  lis: list of object
    :returns:   the first element of the list (or None if lis is None or empty)
    :rtype:     object or value

    """

    if (lis == None) or (len(lis) < 1):
        return None
    return lis[0]


def safe_len(lis):
    """
    Return the number of elements of the list,
    dealing safely with non-list arguments.

    :param lis: a list of objects or values
    :type  lis: list of object
    :returns:   the length of the list (or -1 if lis is not a list)
    :rtype:     int
    """

    try:
        return len(lis)
    except:
        pass
    return -1


def query_xpath(obj, query, args, nsp, required=None, formatted_query=None):
    """
    Perform an xpath query on an XML (`lxml`) node `obj`.

    The `query` template will be formatted using `args`
    and the namespaces `nsp`.
    (This works only in Python 2.6+.)

    If `required` is not None and the result is empty,
    raise an exception.

    If `formatted_query` is passed,
    use it instead of formatting `query` with `args`.
    (Useful if working in Python <2.6.)

    :param obj:             the XML (`lxml`) node object
    :type  obj:             object
    :param query:           a string template to be formatted with args
    :type  query:           str
    :param args:            a list of arguments to format the query
    :type  args:            list of str
    :param nsp:             namespace dictionary,
                            mapping prefixes to namespace strings
    :type  nsp:             dict
    :param required:        required element
    :type  required:        str
    :param formatted_query: a pre-formatted query
    :type  formatted_query: str
    :returns:               the matched XML node objects
    :rtype:                 list of object

    """

    if formatted_query == None:
        xpath_query = query.format(*args)
    else:
        xpath_query = formatted_query
    result = obj.xpath(xpath_query, namespaces=nsp)

    if (required != None) and (len(result) < 1):
        raise Exception("Cannot find '%s' element" % required)

    return result


def parse_viewport_string(string):
    """
    Parse the given viewport value and return
    the corresponding dictionary {"width": W, "height": H}.

    :param string: a viewport value
    :type  string: str
    :returns:      {"width": W, "height": H} or None if `string` is not valid
    :rtype:        dict

    """

    if string != None:
        match = VP_PATTERN_WH.match(string)
        if match != None:
            return {"width": match.group(1), "height": match.group(2)}
        match = VP_PATTERN_HW.match(string)
        if match != None:
            return {"width": match.group(2), "height": match.group(1)}
    return None


def split_reference(string):
    """
    Split the given reference (BASE#F) and return
    a dictionary {"base": BASE, "fragment": F}.

    If there is no fragment, return {"base": BASE}.

    If the string is None, return {}.

    :param string: a reference
    :type  string: str
    :returns:      a dictionary containing base and fragment id
    :rtype:        dict

    """

    # TODO improve this
    if string != None:
        val = string.split("#")
        if len(val) == 2:
            return {"base": val[0], "fragment": val[1]}
        elif len(val) == 1:
            return {"base": val[0], "fragment": None}
    return {}


def is_valid(obj, allowed_class, single=True):
    """
    If `single` is True, return True if
    `obj` is an instance of `allowed_class` or None.

    If `single` is False, return True if
    `obj` is a list (possibly, empty) of instances of `allowed_class`.

    :param obj:           the object to be checked
    :type  obj:           object or list
    :param allowed_class: the allowed class
    :type  allowed_class: class
    :param single:        if True, obj must be a single object
    :type  single:        bool
    :returns:             whether the given object is valid
    :rtype:               bool

    """

    if single:
        if obj == None:
            return True
        return isinstance(obj, allowed_class)
    else:
        if isinstance(obj, list):
            if len(obj) == 0:
                return True
            for element in obj:
                if not isinstance(element, allowed_class):
                    return False
            return True
        return False


def obfuscate_data(data, key, algorithm):
    """
    Obfuscate/deobfuscate data with the given key and algorithm.

    :param data:      the data to be obfuscated/deobfuscated
    :type  data:      bytes
    :param key:       the string to be used as the obfuscation key
    :type  key:       str
    :param algorithm: the algorithm to be used ("adobe" or "idpf")
    :type  algorithm: str
    :rtype:           bytes
    """

    if algorithm == Obfuscation.ADOBE:
        outer_max = 64
        inner_max = 16
        clean_key = key
        clean_key = clean_key.replace(u"urn:uuid:", "") # TODO check this
        clean_key = clean_key.replace(u"-", "")
        clean_key = clean_key.replace(u":", "")
        digest = clean_key
    elif algorithm == Obfuscation.IDPF:
        outer_max = 52
        inner_max = 20
        clean_key = key
        clean_key = clean_key.replace(u"\u0020", "")
        clean_key = clean_key.replace(u"\u0009", "")
        clean_key = clean_key.replace(u"\u000d", "")
        clean_key = clean_key.replace(u"\u000a", "")
        try:
            # Python 2
            digest = hashlib.sha1(clean_key).digest()
        except:
            # Python 3
            digest = hashlib.sha1(clean_key.encode("utf-8")).digest()
    else:
        return None

    if type(data) == str:
        # Python 2
        byte_data = bytearray(data)
    else:
        # Python 3
        byte_data = data

    if type(digest) == str:
        # Python 2
        key_data = bytearray(digest)
    else:
        # Python 3
        key_data = digest

    key_size = len(key_data)
    i = 0
    outer = 0
    accumulator = bytearray()
    while (outer < outer_max) and (i < len(byte_data)):
        inner = 0
        while (inner < inner_max) and (i < len(byte_data)):
            source_byte = byte_data[i]
            key_byte = key_data[inner % key_size]
            obfuscated_byte = source_byte ^ key_byte
            accumulator.append(obfuscated_byte)
            inner += 1
            i += 1
        outer += 1
    while i < len(byte_data):
        accumulator.append(byte_data[i])
        i += 1
    return bytes(accumulator)


def clip_time_seconds(string):
    """
    Convert the given clip time string in seconds
    (possibly with decimal digits).

    :param string: the clip time string to be converted
    :type  string: str
    :returns:      the clip time in seconds
    :rtype:        float
    """
    if (string == None) or (len(string) < 1):
        return 0
    value = 0
    if "ms" in string:
        value = float(string.replace("ms", "")) * 0.001
    elif "s" in string:
        value = float(string.replace("s", ""))
    elif "h" in string:
        value = float(string.replace("h", "")) * 3600
    elif "min" in string:
        value = float(string.replace("min", "")) * 60
    else:
        v_h = 0
        v_m = 0
        v_s = 0
        v_d = 0
        str_hms = string
        if "." in str_hms:
            str_hms, str_d = str_hms.split(".")
            if len(str_d) > 0:
                v_d = 1.0 * int(str_d) / (10 ** len(str_d))
        arr_hms = str_hms.split(":")
        v_n = len(arr_hms)
        if v_n >= 1:
            v_s = int(arr_hms[-1])
        if v_n >= 2:
            v_m = int(arr_hms[-2])
        if v_n >= 3:
            v_h = int(arr_hms[-3])
        value = v_h * 3600 + v_m * 60 + v_s + v_d
    return value


