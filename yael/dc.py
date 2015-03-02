#!/usr/bin/env python
# coding=utf-8

"""
Dublin Core constants.
"""

from yael.namespace import Namespace

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.5"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class DC:
    """
    Enumeration of Dublin Core constants.

    See the source code for the complete list.
    """

    E_CONTRIBUTOR = "contributor"
    E_COVERAGE = "coverage"
    E_CREATOR = "creator"
    E_DATE = "date"
    E_DESCRIPTION = "description"
    E_FORMAT = "format"
    E_IDENTIFIER = "identifier"
    E_LANGUAGE = "language"
    E_PUBLISHER = "publisher"
    E_RELATION = "relation"
    E_RIGHTS = "rights"
    E_SOURCE = "source"
    E_SUBJECT = "subject"
    E_TITLE = "title"
    E_TYPE = "type"
    E_NS_CONTRIBUTOR = "{{{0}}}{1}".format(Namespace.DC, E_CONTRIBUTOR)
    E_NS_COVERAGE = "{{{0}}}{1}".format(Namespace.DC, E_COVERAGE)
    E_NS_CREATOR = "{{{0}}}{1}".format(Namespace.DC, E_CREATOR)
    E_NS_DATE = "{{{0}}}{1}".format(Namespace.DC, E_DATE)
    E_NS_DESCRIPTION = "{{{0}}}{1}".format(Namespace.DC, E_DESCRIPTION)
    E_NS_FORMAT = "{{{0}}}{1}".format(Namespace.DC, E_FORMAT)
    E_NS_IDENTIFIER = "{{{0}}}{1}".format(Namespace.DC, E_IDENTIFIER)
    E_NS_LANGUAGE = "{{{0}}}{1}".format(Namespace.DC, E_LANGUAGE)
    E_NS_PUBLISHER = "{{{0}}}{1}".format(Namespace.DC, E_PUBLISHER)
    E_NS_RELATION = "{{{0}}}{1}".format(Namespace.DC, E_RELATION)
    E_NS_RIGHTS = "{{{0}}}{1}".format(Namespace.DC, E_RIGHTS)
    E_NS_SOURCE = "{{{0}}}{1}".format(Namespace.DC, E_SOURCE)
    E_NS_SUBJECT = "{{{0}}}{1}".format(Namespace.DC, E_SUBJECT)
    E_NS_TITLE = "{{{0}}}{1}".format(Namespace.DC, E_TITLE)
    E_NS_TYPE = "{{{0}}}{1}".format(Namespace.DC, E_TYPE)
    V_DCTERMS_MODIFIED = "dcterms:modified"

    ALL_ELEMENTS = [
        E_CONTRIBUTOR,
        E_COVERAGE,
        E_CREATOR,
        E_DATE,
        E_DESCRIPTION,
        E_FORMAT,
        E_IDENTIFIER,
        E_LANGUAGE,
        E_PUBLISHER,
        E_RELATION,
        E_RIGHTS,
        E_SOURCE,
        E_SUBJECT,
        E_TITLE,
        E_TYPE,
    ]

    ALL_NS_ELEMENTS = [
        E_NS_CONTRIBUTOR,
        E_NS_COVERAGE,
        E_NS_CREATOR,
        E_NS_DATE,
        E_NS_DESCRIPTION,
        E_NS_FORMAT,
        E_NS_IDENTIFIER,
        E_NS_LANGUAGE,
        E_NS_PUBLISHER,
        E_NS_RELATION,
        E_NS_RIGHTS,
        E_NS_SOURCE,
        E_NS_SUBJECT,
        E_NS_TITLE,
        E_NS_TYPE,
    ]


