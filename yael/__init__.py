#!/usr/bin/env python
# coding=utf-8

"""
**yael** (Yet Another EPUB Library) is a Python library
for reading, manipulating, and writing EPUB 2/3 files.
"""

from yael.asset import Asset
from yael.container import Container
from yael.dc import DC
from yael.element import Element
from yael.encryption import Encryption
from yael.enckey import EncKey
from yael.epub import EPUB
from yael.jsonable import JSONAble
from yael.manifestation import Manifestation
from yael.marcrelator import MARCRelator
from yael.mediatype import MediaType
from yael.metadata import Metadata
from yael.moaudio import MOAudio
from yael.modocument import MODocument
from yael.mopar import MOPar
from yael.moseq import MOSeq
from yael.motext import MOText
from yael.namespace import Namespace
from yael.navdocument import NavDocument
from yael.navelement import NavElement
from yael.navnode import NavNode
from yael.ncxtoc import NCXToc
from yael.ncxtocnode import NCXTocNode
from yael.obfuscation import Obfuscation
from yael.opfdc import OPFDC
from yael.opfguide import OPFGuide
from yael.opfitem import OPFItem
from yael.opfitemref import OPFItemref
from yael.opflink import OPFLink
from yael.opfmanifest import OPFManifest
from yael.opfmeta2 import OPFMeta2
from yael.opfmeta3 import OPFMeta3
from yael.opfmetadata import OPFMetadata
from yael.opfmetadatum import OPFMetadatum
from yael.opfpacdocument import OPFPacDocument
from yael.opfreference import OPFReference
from yael.opfspine import OPFSpine
from yael.pacdocument import PacDocument
from yael.parsing import Parsing
from yael.publication import Publication
from yael.rendition import Rendition
from yael.rmdocument import RMDocument
from yael.rmlocation import RMLocation
from yael.rmpoint import RMPoint
from yael.simpleepub import SimpleEPUB
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.5"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"
