Multiple Posting
================

.. post:: Jun 10, 2014
   :tags: directive
   :category: Manual
   :location: SF
   :author: Ahmet

:rst:dir:`post` directive now can be used multiple times in a single page
to create multiple posts of different sections of the document.



Posting a Section
-----------------

.. post:: Jun 10, 2014
   :tags: directive
   :category: Manual
   :location: SF
   :author: Ahmet

Second time a document is posted, post title and excerpt will be extracted
from the section in which the :rst:dir:`post` directive resides.

The section post will be treated like any other document post, except:

  * Next and previous links at the bottom will only regard the first post
    in the document,
  * ...