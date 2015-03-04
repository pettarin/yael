#!/usr/bin/env python
# coding=utf-8

"""
EPUB constants.
"""

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "0.0.9"
__email__ = "alberto@albertopettarin.it"
__status__ = "Development"

class EPUB:
    """
    Enumeration of EPUB constants:
    reserved internal paths and EPUB 3 Semantic Vocabulary.

    See the source code for the complete list.
    """

    INTERNAL_PATH_CONTAINER_XML = "META-INF/container.xml"
    INTERNAL_PATH_ENCRYPTION_XML = "META-INF/encryption.xml"
    INTERNAL_PATH_MANIFEST_XML = "META-INF/manifest.xml"
    INTERNAL_PATH_METADATA_XML = "META-INF/metadata.xml"
    INTERNAL_PATH_META_INF = "META-INF"
    INTERNAL_PATH_MIMETYPE = "mimetype"
    INTERNAL_PATH_RIGHTS_XML = "META-INF/rights.xml"
    INTERNAL_PATH_SIGNATURES_XML = "META-INF/signatures.xml"

    VOCABULARY = {
        # Document partitions
        "cover"                       : "cover",
        "frontmatter"                 : "frontmatter",
        "bodymatter"                  : "bodymatter",
        "backmatter"                  : "backmatter",

        # Document divisions
        "volume"                      : "volume",
        "part"                        : "part",
        "chapter"                     : "chapter",
        "subchapter"                  : "subchapter",
        "division"                    : "division",

        # Document sections and components
        "abstract"                    : "abstract",
        "foreword"                    : "foreword",
        "preface"                     : "preface",
        "prologue"                    : "prologue",
        "introduction"                : "introduction",
        "preamble"                    : "preamble",
        "conclusion"                  : "conclusion",
        "epilogue"                    : "epilogue",
        "afterword"                   : "afterword",
        "epigraph"                    : "epigraph",

        # Document navigation
        "toc"                         : "toc",
        "toc-brief"                   : "toc-brief",
        "landmarks"                   : "landmarks",
        "loa"                         : "loa",
        "loi"                         : "loi",
        "lot"                         : "lot",
        "lov"                         : "lov",

        # Document reference sections
        "appendix"                    : "appendix",
        "colophon"                    : "colophon",
        "credits"                     : "credits",
        "keywords"                    : "keywords",
        # Indexes
        "index"                       : "index",
        "index-headnotes"             : "index-headnotes",
        "index-legend"                : "index-legend",
        "index-group"                 : "index-group",
        "index-entry-list"            : "index-entry-list",
        "index-entry"                 : "index-entry",
        "index-term"                  : "index-term",
        "index-editor-note"           : "index-editor-note",
        "index-locator"               : "index-locator",
        "index-locator-list"          : "index-locator-list",
        "index-locator-range"         : "index-locator-range",
        "index-xref-preferred"        : "index-xref-preferred",
        "index-xref-related"          : "index-xref-related",
        "index-term-category"         : "index-term-category",
        "index-term-categories"       : "index-term-categories",
        # Glossaries
        "glossary"                    : "glossary",
        "glossterm"                   : "glossterm",
        "glossdef"                    : "glossdef",
        # Bibliographies
        "bibliography"                : "bibliography",
        "biblioentry"                 : "biblioentry",

        # Preliminary sections and components
        "titlepage"                   : "titlepage",
        "halftitlepage"               : "halftitlepage",
        "copyright-page"              : "copyright-page",
        "seriespage"                  : "seriespage",
        "acknowledgments"             : "acknowledgments",
        "imprint"                     : "imprint",
        "imprimatur"                  : "imprimatur",
        "contributors"                : "contributors",
        "other-credits"               : "other-credits",
        "errata"                      : "errata",
        "dedication"                  : "dedication",
        "revision-history"            : "revision-history",

        # Complementary content
        "case-study"                  : "case-study",
        "help"                        : "help",
        "marginalia"                  : "marginalia",
        "notice"                      : "notice",
        "pullquote"                   : "pullquote",
        "sidebar"                     : "sidebar",
        "warning"                     : "warning",

        # Titles and headings
        "halftitle"                   : "halftitle",
        "fulltitle"                   : "fulltitle",
        "covertitle"                  : "covertitle",
        "title"                       : "title",
        "subtitle"                    : "subtitle",
        "label"                       : "label",
        "ordinal"                     : "ordinal",
        "bridgehead"                  : "bridgehead",

        # Educational content
        # Learning objectives
        "learning-objective"          : "learning-objective",
        "learning-objectives"         : "learning-objectives",
        "learning-outcome"            : "learning-outcome",
        "learning-outcomes"           : "learning-outcomes",
        "learning-resource"           : "learning-resource",
        "learning-resources"          : "learning-resources",
        "learning-standard"           : "learning-standard",
        "learning-standards"          : "learning-standards",
        # Testing
        "answer"                      : "answer",
        "answers"                     : "answers",
        "assessment"                  : "assessment",
        "assessments"                 : "assessments",
        "feedback"                    : "feedback",
        "fill-in-the-blank-problem"   : "fill-in-the-blank-problem",
        "general-problem"             : "general-problem",
        "qna"                         : "qna",
        "match-problem"               : "match-problem",
        "multiple-choice-problem"     : "multiple-choice-problem",
        "practice"                    : "practice",
        "practices"                   : "practices",
        "question"                    : "question",
        "true-false-problem"          : "true-false-problem",

        # Comics
        "panel"                       : "panel",
        "panel-group"                 : "panel-group",
        "balloon"                     : "balloon",
        "text-area"                   : "text-area",
        "sound-area"                  : "sound-area",

        # Notes and annotations
        "annotation"                  : "annotation",
        "note"                        : "note",
        "footnote"                    : "footnote",
        "rearnote"                    : "rearnote",
        "footnotes"                   : "footnotes",
        "rearnotes"                   : "rearnotes",

        # References
        "annoref"                     : "annoref",
        "biblioref"                   : "biblioref",
        "glossref"                    : "glossref",
        "noteref"                     : "noteref",
        "referrer"                    : "referrer",

        # Document text
        "credit"                      : "credit",
        "keyword"                     : "keyword",
        "topic-sentence"              : "topic-sentence",
        "concluding-sentence"         : "concluding-sentence",

        # Pagination
        "pagebreak"                   : "pagebreak",
        "page-list"                   : "page-list",

        # Tables
        "table"                       : "table",
        "table-row"                   : "table-row",
        "table-cell"                  : "table-cell",

        # Lists
        "list"                        : "list",
        "list-item"                   : "list-item",

        # Figures
        "figure"                      : "figure",
    }


