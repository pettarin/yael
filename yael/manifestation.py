#!/usr/bin/env python
# coding=utf-8

"""
Manifestation constants.
"""

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.2"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Manifestation:
    """
    Enumeration of values for the
    manifestation of a :class:`yael.publication.Publication`.
    """

    COMPRESSED = "compressed"
    """ The :class:`yael.publication.Publication`
    is loaded from a compressed file. """

    MEMORY = "memory"
    """ The :class:`yael.publication.Publication`
    is being built programmatically.  """

    UNCOMPRESSED = "uncompressed"
    """ The :class:`yael.publication.Publication`
    is loaded from an uncompressed directory. """



