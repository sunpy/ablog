
Deploy to GitHub Pages
======================


.. post:: Apr 07, 2015
   :tags: deploy
   :author: Ahmet
   :category: Manual
   :location: SF

If you are looking for a place to publish your blog, `GitHub Pages`__ might be the place for you.

__ https://pages.github.com/

Assuming that you have a GitHub account, here are what you need to do to get published:

1. Head over to GitHub_ and create a new repository named ``username.github.io``, where username is your username (or organization name) on GitHub.

2. (optional) If you followed the link, you might as well give a star to ABlog ;)

3. Set :confval:`github_pages` configuration variable in :file:`conf.py` file.

4. Run ``ablog build`` in your project folder.

5. Run ``ablog deploy``. This command will

   i. clone your GitHub pages repository to project folder,

   ii. copy all files from build folder (:file:`_website`) to :file:`username.github.io`,

   iii. add and commit copied files,

   iv. add `.nojekyll <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#troubleshooting-publishing-from-a-branch>`_
       file, since this ain't no Jekyll_

   v. and finally push the changes to publish.

Let us know how this works for you!

.. _Jekyll: https://jekyllrb.com/
