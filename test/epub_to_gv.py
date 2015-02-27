#!/usr/bin/python

"""
Print the directed network graph for a given EPUB ebook.

The output, printed to stdout, is in graphviz (dot) format.

The nodes are the spine items, identified by their manifest id.

The black arcs are direct links between content documents,
the red arcs show the spine progression.
"""

# standard modules
import bs4
import os
import sys

# yael modules
# TODO find a better way to do this
PROJECT_DIRECTORY = os.path.dirname(
    os.path.dirname(os.path.realpath(sys.argv[0])))
sys.path.append(PROJECT_DIRECTORY)
from yael import DC
from yael import MediaType
from yael import OPFMeta3
from yael import Parsing 
from yael import Publication 
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.2"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

def usage():
    print("")
    print("$ ./%s path/to/dir [--no-spine] > path/to/out.gv" % sys.argv[0])
    print("$ ./%s path/to/file.epub [--no-spine] > path/to/out.gv" % sys.argv[0])
    print("")

def main():
    if len(sys.argv) > 1:
        p = Publication(
            path=sys.argv[1],
            parsing_options=[Parsing.NO_MEDIA_OVERLAY])
    else:
        usage()
        return

    add_spine = True
    if (len(sys.argv) > 2) and (sys.argv[2] == "--no-spine"):
        add_spine = False

    arcs = []
    pac_document = p.container.default_rendition.pac_document
    manifest = pac_document.manifest
    spine = pac_document.spine.itemrefs
    for itemref in spine:
        item = manifest.item_by_id(itemref.v_idref)
        if item != None:
            i_p_item = item.asset.internal_path
            try:
                soup = bs4.BeautifulSoup(item.contents)
                for link in soup.find_all('a'):
                    target_href = link.get('href')
                    if (
                            (target_href != None) and
                            (not target_href.startswith("http"))):
                        i_p_target = yael.util.norm_join_parent(
                            i_p_item,
                            target_href.split("#")[0])
                        target = manifest.item_by_internal_path(i_p_target)
                        if target != None:
                            arcs.append([item.v_id, target.v_id, "link"])
            except:
                pass

    if add_spine:
        for i in range(len(spine)):
            if i+1 < len(spine):
                item = pac_document.manifest.item_by_id(spine[i].v_idref)
                target = pac_document.manifest.item_by_id(spine[i+1].v_idref)
                arcs.append([item.v_id, target.v_id, "spine"])

    print("digraph book {")
    for arc in arcs:
        if arc[2] == "link":
            color = ""
        else:
            color = " [color=red]"
        print('"%s" -> "%s"%s;' % (arc[0], arc[1], color))
    print("}")



if __name__ == '__main__':
    main()



