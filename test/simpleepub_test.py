#!/usr/bin/python

"""
SimpleEPUB test
"""

# standard modules
import os
import sys

# yael modules
# TODO find a better way to do this
PROJECT_DIRECTORY = os.path.dirname(
    os.path.dirname(os.path.realpath(sys.argv[0])))
sys.path.append(PROJECT_DIRECTORY)
from yael import Parsing
from yael import SimpleEPUB

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

def usage():
    print("")
    print("$ ./%s path/to/dir [--no-mo]" % sys.argv[0])
    print("$ ./%s path/to/file.epub [--no-mo]" % sys.argv[0])
    print("")

def main():
    if (len(sys.argv) > 2) and (sys.argv[2] == "--no-mo"):
        p = SimpleEPUB(
            path=sys.argv[1],
            parsing_options=[Parsing.NO_MEDIA_OVERLAY])
    elif len(sys.argv) > 1:
        p = SimpleEPUB(
            path=sys.argv[1],
            parsing_options=[])
    else:
        usage()
        return

    print("")
    print("Manifestation       = %s" % p.manifestation)
    print("Version             = %s" % p.version)
    print("Unique identifier   = %s" % p.unique_identifier)
    print("dcterms:modified    = %s" % p.dcterms_modified)
    print("Release identifier  = %s" % p.release_identifier)
    print("")
    print("Internal path cover = %s" % p.internal_path_cover_image)
    print("")
    print("Title               = %s" % p.title)
    print("Language            = %s" % p.language)
    print("Author              = %s" % p.author)
    print("Date                = %s" % p.date)
    print("Description         = %s" % p.description)
    print("Publisher           = %s" % p.publisher)
    print("Rights              = %s" % p.rights)
    print("Source              = %s" % p.source)
    print("Subjects            = %s" % ", ".join(sorted(p.subjects)))
    print("Type                = %s" % p.type)
    print("")

    # print the TOC
    #print(p.toc)

    # print the TOC with resolved paths
    #print(p.resolved_toc)

    # print the landmarks
    #print(p.landmarks)

    # print the landmarks with resolved paths
    #print(p.resolved_landmarks)

    # print the spine
    #print("Spine")
    #for i_p_spine_item in p.resolved_spine:
    #    print(i_p_spine_item)
    #print("")

    # print the spine (linear="yes" or omitted)
    #print("Spine (linear)")
    #for i_p_spine_item in p.resolved_spine_linear:
    #    print(i_p_spine_item)
    #print("")

    # get the contents of META-INF/container.xml
    #print("Contents of META-INF/container.xml")
    #print("")
    #print(p.asset_contents("META-INF/container.xml"))
    #print("")

    # get the contents of another asset
    #print("Contents of OEBPS/Text/p001.xhtml")
    #print("")
    #print(p.asset_contents("OEBPS/Text/p001.xhtml"))
    #print("")

    # extract cover image to /tmp/extracted_cover.jpg
    #cover_image = p.cover_image
    #if cover_image != None:
    #    output_file = open("/tmp/extracted_cover.jpg", "wb")
    #    output_file.write(cover_image)
    #    output_file.close()
    #    print("Cover image extracted to '/tmp/extracted_cover.jpg' ...")

if __name__ == '__main__':
    main()



