#!/usr/bin/env python
# coding=utf-8

"""
The OPF `<manifest>` element.
"""

from yael.element import Element
from yael.jsonable import JSONAble
from yael.mediatype import MediaType
from yael.namespace import Namespace
from yael.opfitem import OPFItem
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.2"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class OPFManifest(Element):
    """
    Build the OPF `<manifest>` element or
    parse it from `obj` or `string`.
    """

    A_ID = "id"
    E_ITEM = "item"

    def __init__(self, internal_path=None, obj=None, string=None):
        self.v_id = None
        self.items = []
        Element.__init__(
            self,
            internal_path=internal_path,
            obj=obj,
            string=string)

    def parse_object(self, obj):
        # get attributes
        self.v_id = obj.get(OPFManifest.A_ID)

        # locate `<item>` elements
        item_arr = yael.util.query_xpath(
            obj=obj,
            query="{0}:{1}",
            args=["o", OPFManifest.E_ITEM],
            nsp={"o": Namespace.OPF, "x": Namespace.XML},
            required=None)
        for item in item_arr:
            try:
                item_parsed = OPFItem(obj=item)
                if (
                        (self.internal_path != None) and
                        (item_parsed.v_href != None)):
                    item_parsed.internal_path = yael.util.norm_join_parent(
                        self.internal_path, item_parsed.v_href)
                self.add_item(item_parsed)
            except:
                pass

    def json_object(self, recursive=True):
        obj = {
            "id":    self.v_id,
            "items": len(self.items),
        }
        if recursive:
            obj["items"] = JSONAble.safe(self.items)
        return obj

    def __len__(self):
        return len(self.items)

    def add_item(self, item):
        """
        Add the given `<item>` to the manifest.

        :param item: the `<item>` to be added
        :type  item: :class:`yael.opfitem.OPFItem`
        """
        self.items.append(item)

    def item_by_id(self, v_id):
        """
        Return the `<item>` child with given `id`.

        :param v_id: the desired `id`
        :type  v_id: str
        :returns:    the child with given id, or None if not found
        :rtype:      :class:`yael.opfitem.OPFItem`
        """
        lis = list(e for e in self.items if e.v_id == v_id)
        return yael.util.safe_first(lis)

    def items_by_media_type(self, v_media_type):
        """
        Return the `<item>` child with given `media-type`.

        :param v_media_type: the desired `media-type`
        :type  v_media_type: str
        :returns:            the child with given media-type,
                             or None if not found
        :rtype:              :class:`yael.opfitem.OPFItem`
        """
        return list(e for e in self.items if e.v_media_type == v_media_type)

    def item_by_internal_path(self, internal_path):
        """
        Return the `<item>` child with href corresponding
        to the given internal path.

        :param internal_path: the internal path of the desired item
        :type  internal_path: str
        :returns:             the child with given path, or None if not found
        :rtype:               :class:`yael.opfitem.OPFItem`
        """
        lis = list(e for e in self.items if e.internal_path == internal_path)
        return yael.util.safe_first(lis)

    @property
    def v_id(self):
        """
        The value of the `id` attribute.

        :rtype: str
        """
        return self.__v_id

    @v_id.setter
    def v_id(self, v_id):
        self.__v_id = v_id

    @property
    def items(self):
        """
        The list of `<item>` objects in this manifest.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return self.__items

    @items.setter
    def items(self, items):
        self.__items = items

    @property
    def cover_image_item(self):
        """
        The item with property `cover-image`.

        :rtype: :class:`yael.opfitem.OPFItem`
        """

        for item in self.items:
            if (
                    (item.v_properties != None) and
                    (OPFItem.V_COVER_IMAGE in item.v_properties.split(" "))):
                return item
        return None

    @property
    def nav_document_item(self):
        """
        The item with property `nav`.

        :rtype: :class:`yael.opfitem.OPFItem`
        """

        for item in self.items:
            if (
                    (item.v_properties != None) and
                    (OPFItem.V_NAV in item.v_properties.split(" "))):
                return item
        return None

    @property
    def audio_items(self):
        """
        The list of items with `media-type` associated with audio formats.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if MediaType.is_audio(e.v_media_type))

    @property
    def content_document_items(self):
        """
        The list of items corresponding to Content Documents.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if MediaType.is_content_document(
            e.v_media_type))

    @property
    def font_items(self):
        """
        The list of items with `media-type` associated with font formats.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if MediaType.is_font(e.media_type))

    @property
    def image_items(self):
        """
        The list of items with `media-type` associated with image formats.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if MediaType.is_image(e.v_media_type))

    @property
    def video_items(self):
        """
        The list of items with `media-type` associated with video formats.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if MediaType.is_video(e.v_media_type))

    @property
    def scripted_items(self):
        """
        The list of items corresponding to Scripted Documents.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if e.has_property(OPFItem.V_SCRIPTED))

    @property
    def mathml_items(self):
        """
        The list of items with MathML elements.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if e.has_property(OPFItem.V_MATHML))

    @property
    def svg_items(self):
        """
        The list of items with SVG elements.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if e.has_property(OPFItem.V_SVG))

    @property
    def mo_items(self):
        """
        The list of items with Media Overlays.

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if e.v_media_overlay != None)

    @property
    def smil_items(self):
        """
        The list of items corresponding to Media Overlay Documents (SMIL).

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return list(e for e in self.items if e.v_media_type == MediaType.SMIL)

    @property
    def mo_document_items(self):
        """
        The list of items corresponding to Media Overlay Documents (SMIL).

        :rtype: list of :class:`yael.opfitem.OPFItem` objects
        """
        return self.smil_items



