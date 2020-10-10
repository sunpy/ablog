
Deploy to GitHub Pages
======================


.. post:: Apr 07, 2015
   :tags: deploy
   :author: Ahmet
   :category: Manual
   :location: SF

If you are looking for a place to publish your blog, `GitHub Pages`_ might be the place for you.

.. _GitHub Pages: https://pages.github.com/

Assuming that you have a GitHub account, here are what you need to do to get published:

1. Head over to GitHub_ and create a new repository named ``username.github.io``, where username is your username (or organization name) on GitHub.

2. (optional) If you followed the link, you might as well give a star to ABlog ;)

3. Set :confval:`github_pages` configuration variable in :file:`conf.py` file.

4. Run ``ablog build`` in your project folder.

5. Run ``ablog deploy``. This command will

   i. clone your GitHub pages repository to project folder,

   ii. copy all files from build folder (:file:`_website`) to :file:`username.github.io`,

   iii. add and commit copied files,

   iv. add `.nojekyll <https://help.github.com/articles/using-jekyll-with-pages/#turning-jekyll-off>`_
       file, since this ain't no Jekyll_

   v. and finally push the changes to publish.

Let us know how this works for you!

.. _Jekyll: https://jekyllrb.com/
