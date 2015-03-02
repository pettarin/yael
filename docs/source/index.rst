Package **yael**
================

.. automodule:: yael


Usage
-----

>>> from yael import SimpleEPUB
>>> ebook = SimpleEPUB(path="/tmp/bierce01.epub")
>>> ebook.manifestation
'compressed'
>>> ebook.size
7281362
>>> ebook.version
'3.0'
>>> ebook.unique_identifier
'urn:uuid:2722b0eb-a4f9-4b05-97f9-9123381e58b3'
>>> ebook.release_identifier
'urn:uuid:2722b0eb-a4f9-4b05-97f9-9123381e58b3@2014-06-06T00:00:01Z'
>>> ebook.title
'A Horseman In The Sky'
>>> ebook.language
'en'
>>> ebook.author
'Ambrose Bierce'
>>> ebook.date
'2014-06-06'
>>> ebook.description
'This Audio-eBook was crafted by ReadBeyond to celebrate the release of Menestrello, a free app for reading+listening Audio-eBooks in EPUB 3 reflowable format. For more information, please visit http://www.readbeyond.it/menestrello/'
>>> ebook.publisher
'ReadBeyond'
>>> ebook.internal_path_cover_image
'OEBPS/Images/cover.png'
>>> print(ebook) # print a JSON string representation
(...)
>>> print(ebook.resolved_toc) # print the TOC with resolved paths
(...)
>>> print("Spine")
>>> for i_p_spine_item in ebook.resolved_spine:
>>>     print(i_p_spine_item)
>>>     print("")
(...)
>>> cover_image = ebook.cover_image
>>> if cover_image != None:
>>>     output_file = open("/tmp/extracted_cover.jpg", "wb")
>>>     output_file.write(cover_image)
>>>     output_file.close()
>>>     print("Cover image extracted to '/tmp/extracted_cover.jpg' ...")


Classes
-------

.. toctree::
    :maxdepth: 3

    asset
    container
    dc
    element
    encdata
    enckey
    encryption
    epub
    jsonable
    manifestation
    marcrelator
    mediatype
    metadata
    moaudio
    modocument
    mopar
    moseq
    motext
    namespace
    navdocument
    navelement
    navnode
    ncxtoc
    ncxtocnode
    obfuscation
    opfdc
    opfguide
    opfitem
    opfitemref
    opflink
    opfmanifest
    opfmeta2
    opfmeta3
    opfmetadata
    opfmetadatum
    opfpacdocument
    opfreference
    opfspine
    pacdocument
    parsing
    publication
    rendition
    rmdocument
    rmlocation
    rmpoint
    simpleepub
    util



Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


