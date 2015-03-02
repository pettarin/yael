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
from yael import Parsing
from yael import Publication
import yael.util

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.7"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

def usage():
    print("")
    print("$ ./%s path/to/dir [--no-spine] > path/to/out.gv" % sys.argv[0])
    print("$ ./%s path/to/file.epub [--no-spine] > path/to/out.gv" % sys.argv[0])
    print("")

def main():
    if len(sys.argv) > 1:
        # read from file.epub or uncompressed dir
        # parsing MO is not necessary
        ebook = Publication(
            path=sys.argv[1],
            parsing_options=[Parsing.NO_MEDIA_OVERLAY])
    else:
        # no arguments => print usage
        usage()
        return

    # shall we add the arcs showing the spine progression?
    add_spine = True
    if (len(sys.argv) > 2) and (sys.argv[2] == "--no-spine"):
        add_spine = False

    # arc accumulator
    arcs = []

    # shortcuts
    pac_document = ebook.container.default_rendition.pac_document
    manifest = pac_document.manifest
    spine = pac_document.spine.itemrefs

    # for each item in the spine...
    for itemref in spine:
        item = manifest.item_by_id(itemref.v_idref)
        if item != None:
            i_p_item = item.asset.internal_path
            try:
                # ...read the item contents and try to load it
                # as a tag soup using BeautifulSoup...
                soup = bs4.BeautifulSoup(item.contents)

                # ... finding all the <a> elements...
                for link in soup.find_all('a'):
                    # ... that have an href attribute
                    target_href = link.get('href')
                    if (
                            (target_href != None) and
                            (not target_href.startswith("http"))):
                        # get the internal path of the target file,
                        # removing the #fragment, if any
                        i_p_target = yael.util.norm_join_parent(
                            i_p_item,
                            target_href.split("#")[0])
                        # get the manifest id of the target file
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

    # output to stdout in Graphviz (dot) format
    # use redirection to save to file, i.e.:
    #
    # digraph book {
    # "a" -> "b";
    # "b" -> "a";
    # "b" -> "c";
    # "c" -> "b";
    # "a" -> "b" [color=red];
    # }
    #
    # TODO one might want to output a similar graph
    #      showing referenced assets (images, audio, etc.),
    #      not just <a> links
    # TODO mark linear="no" nodes with a special symbol
    # TODO remove/compact/weight duplicate arcs
    #
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



