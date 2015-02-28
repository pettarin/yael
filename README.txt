yael
====

**yael** (Yet Another EPUB Library) is a Python library for reading,
manipulating, and writing EPUB 2/3 files.

-  Version: 0.0.2
-  Date: 2015-02-28
-  Developer: `Alberto Pettarin <http://www.albertopettarin.it/>`__
   (`contact <http://www.albertopettarin.it/contact.html>`__)
-  License: the MIT License (MIT)

Usage
-----

This library is currently in **development**.

The reading part is essentially complete, while the editing/writing is
missing.

Please do **NOT** use this code in production until it reaches v1.0.0.

Feedback (especially on the API/interface) is welcome at any version
number!

See ```test/publication_test.py`` <test/publication_test.py>`__,
```test/simpleepub_test.py`` <test/simpleepub_test.py>`__, and
```test/epub_to_gv.py`` <test/epub_to_gv.py>`__ for usage examples.

Documentation
-------------

Online: http://www.albertopettarin.it/yael/

Generated from the source (requires sphinx):

::

    $ git clone https://github.com/pettarin/yael.git
    $ cd yael/docs
    $ make clean
    $ make html

License
-------

**yael** is released under the terms of the MIT License. See the LICENSE
file.

Supported Features
------------------

Parsing nearly all of EPUB 2 and 3 OCF/OPF specifications, including:

-  EPUB 2 ``<meta>`` and ``<guide>`` OPF elements
-  EPUB 3 ``<meta>`` (including ``refines``)
-  EPUB 3 Media Overlays (SMIL files)
-  EPUB 3 Navigation Document (including ``<nav>`` elements other than
   ``toc`` and ``landmarks``)
-  EPUB 3 Multiple Renditions
-  Asset obfuscation with either Adobe or IDPF algorithms

Other useful stuff:

-  Loadind/saving publications in compressed, uncompressed, or in-memory
   form
-  Retrieving ``viewport`` information from Content Documents in FXL
   EPUB files
-  Building sub-objects from strings
-  Outputting a JSON representation of any object
-  Resolution of MARC Relator values
-  Conversion of SMIL clip times from string to seconds

Limitations and Missing Features
--------------------------------

-  EPUB OCF elements not parsed: ``manifest.xml``, ``rights.xml``,
   ``signatures.xml``
-  EPUB 3 OPF elements not parsed: ``<bindings>``, ``<collection>``
-  No EPUB CFI support
-  No editing of SVG Content Documents

Similar Libraries
-----------------

-  `epub <https://pypi.python.org/pypi/epub>`__
-  `epubzilla <https://pypi.python.org/pypi/Epubzilla>`__
-  `py-clave <https://github.com/gabalese/py-clave>`__

Acknowledgments
---------------

Many thanks to:

-  *Yael*, of course.

|Analytics|

.. |Analytics| image:: https://ga-beacon.appspot.com/UA-52776738-1/yael
   :target: http://www.albertopettarin.it
