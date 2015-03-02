#!/usr/bin/env python
# coding=utf-8

"""
Parsing option constants.
"""

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.5"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class Parsing:
    """
    Enumeration of parsing option constants
    to be used when creating a
    :class:`yael.publication.Publication`
    by parsing a file or directory.
    """

    ASSET_REFS = "asset_refs"
    """ Resolve asset references. Default. """

    NO_ASSET_REFS = "no_asset_refs"
    """ Do not resolve asset references. """

    ENCRYPTION = "encryption"
    """ Parse META-INF/encryption.xml, if present. Default. """

    NO_ENCRYPTION = "no_encryption"
    """ Do not parse META-INF/encryption.xml. """

    MEDIA_OVERLAY = "media_overlay"
    """ Parse the Media Overlay Documents (SMIL files), if present. Default. """

    NO_MEDIA_OVERLAY = "no_media_overlay"
    """ Do not parse the Media Overlay Documents (SMIL files). """

    MULTIPLE_RENDITIONS = "multiple_renditions"
    """ Parse META-INF/metadata.xml and Multiple Renditions, if present.
    Default. """

    NO_MULTIPLE_RENDITIONS = "no_multiple_renditions"
    """ Do not parse META-INF/metadata.xml and Multiple Renditions. """

    NCX = "ncx"
    """ Parse the NCX TOC, if present. Default. """

    NO_NCX = "no_ncx"
    """ Do not parse the NCX TOC. """

    NAV = "nav"
    """ Parse the Navigation Document, if present. Default. """

    NO_NAV = "no_nav"
    """ Do not parse the Navigation Document. """


