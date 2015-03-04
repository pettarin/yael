#!/usr/bin/env python
# coding=utf-8

"""
Media Type constants.
"""

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.8"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class MediaType:
    """
    Enumeration of Media Type constants.

    See the source code for the complete list.
    """

    # EPUB 3 Core Media Types
    CSS = "text/css"
    GIF = "image/gif"
    JPEG = "image/jpeg"
    JPG = "image/jpeg" # alias
    JS = "text/javascript"
    MP3 = "audio/mpeg" # alias
    MP4_AUDIO = "audio/mp4"
    MPEG_AUDIO = "audio/mpeg"
    NCX = "application/x-dtbncx+xml"
    OTF = "application/vnd.ms-opentype"
    OTF_ALT = "application/x-font-opentype"
    OTF_ALT_2 = "application/font-otf"
    OTF_ALT_3 = "application/x-font-otf"
    PLS = "application/pls+xml"
    PNG = "image/png"
    SMIL = "application/smil+xml"
    SVG = "image/svg+xml"
    WOFF = "application/font-woff"
    WOFF_ALT = "application/x-font-woff"
    XHTML = "application/xhtml+xml"


    # other useful Media Types
    AAC = "audio/x-aac"
    AVI = "video/avi"
    BMP = "image/bmp"
    CSV = "text/csv"
    DJVU = "image/vnd.djvu"
    DTD = "application/xml-dtd"
    DVI = "application/x-dvi"
    EOT = "application/vnd.ms-fontobject"
    EPUB = "application/epub+zip"
    FLAC = "audio/flac"
    FLV = "video/x-flv"
    GZIP = "application/gzip"
    HTML = "text/html"
    JSON = "application/json"
    MATROSKA = "video/x-matroska"
    MD = "text/x-markdown"
    MP4_VIDEO = "video/mp4"
    MPEG_VIDEO = "video/mpeg"
    OCTET_STREAM = "application/octet-stream"
    OGG = "audio/ogg"
    OPF = "application/oebps-package+xml"
    PDF = "application/pdf"
    PS = "application/postscript"
    QT = "video/quicktime"
    RDF = "application/rdf+xml"
    RSS = "application/rss+xml"
    RTF = "text/rtf"
    SFNT = "application/font-sfnt"
    SOAP = "application/soap+xml"
    SPEEX = "audio/speex"
    TAR = "application/x-tar"
    TIFF = "image/tiff"
    TTF = "application/x-font-ttf"
    TTF_ALT = "application/x-font-truetype"
    TXT = "text/plain"
    VORBIS = "audio/vorbis"
    WAV = "audio/vnd.wave"
    WEBM_AUDIO = "audio/webm"
    WEBM_VIDEO = "video/webm"
    WMV = "video/x-ms-wmv"
    XML = "application/xml" # or "text/xml"
    Z7 = "application/x-7z-compressed"
    ZIP = "application/zip"

    FONTS = [
        EOT,
        OTF,
        OTF_ALT,
        OTF_ALT_2,
        OTF_ALT_3,
        SFNT,
        SVG,
        TTF,
        TTF_ALT,
        WOFF,
        WOFF_ALT
    ]

    CONTENT_DOCUMENTS = [
        SVG,
        XHTML
    ]


    @staticmethod
    def is_audio(media_type):
        """
        Determine if the given Media Type is associated with an audio format.

        :param media_type: a Media Type string
        :type  media_type: str
        :returns:          True if `media_type` starts with `audio/`

        """

        return media_type.startswith("audio/")


    @staticmethod
    def is_content_document(media_type):
        """
        Determine if the given Media Type is associated
        with an EPUB Content Document.

        :param media_type: a Media Type string
        :type  media_type: str
        :returns:          True if `media_type` is a format listed
                           in `CONTENT_DOCUMENTS`

        """
        return media_type in MediaType.CONTENT_DOCUMENTS


    @staticmethod
    def is_font(media_type):
        """
        Determine if the given Media Type is associated with a font format.

        :param media_type: a Media Type string
        :type  media_type: str
        :returns:          True if `media_type` is a format listed in `FONTS`

        """
        return media_type in MediaType.FONTS


    @staticmethod
    def is_image(media_type):
        """
        Determine if the given Media Type is associated with an image format.

        :param media_type: a Media Type string
        :type  media_type: str
        :returns:          True if `media_type` starts with `image/`

        """

        return media_type.startswith("image/")


    @staticmethod
    def is_video(media_type):
        """
        Determine if the given Media Type is associated with a video format.

        :param media_type: a Media Type string
        :type  media_type: str
        :returns:          True if `media_type` starts with `video/`

        """

        return media_type.startswith("video/")


