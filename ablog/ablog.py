"""ABlog classes for handling posts and archives."""

import os
import re

import datetime as dtmod
from datetime import datetime
from unicodedata import normalize

from docutils import nodes
from docutils.io import StringOutput

from sphinx.util.osutil import relative_uri
from sphinx.environment import dummy_reporter

def slugify(s):
    """Slugify *s*."""

    n = normalize('NFKD', unicode(s)).encode('ascii', 'ignore')
    return re.sub(r'[-\s]+', '-', re.sub(r'[^\w\s-]', '', n).strip().lower())

DEBUG = True
CONFIG = [
    ('blog_path', 'blog', True),
    ('blog_title', 'Blog', True),
    ('blog_baseurl', None, True),

    ('blog_feed_subtitle', None, True),
    ('blog_authors', {}, True),
    ('blog_default_author', None, True),
    ('blog_locations', {}, True),
    ('blog_default_location', None, True),

    ('fontawesome_link_cdn', False, True),
    ('fontawesome_included', False, True),
    ('fontawesome_css_file', False, True),

    ('post_date_format', '%b %d, %Y', True),
    ('post_auto_image', 0, True),
    ('post_auto_excerpt', 1, True),
    ('post_redirect_refresh', 5, True),

    ('disqus_shortname', None, True),
    ('disqus_drafts', False, True),
    ('disqus_pages', False, True),
]


TOMORROW = datetime.today() + dtmod.timedelta(1)
FUTURE = datetime(9999, 12, 31)


class ABlog(object):

    """Handle blog operations."""

    _dict = {}

    def __init__(self, app=None):

        self.__dict__ = self._dict
        if not self._dict:
            self._init(app)

    def _init(self, app):

        self.app = app
        self.std_domain = self.app.env.domains['std']
        self.config = {}

        for opt in CONFIG:
            self.config[opt[0]] = getattr(app.config, opt[0])



        opt = self.config['blog_default_author']
        if opt is not None and not isinstance(opt, list):
            self.config['blog_default_author'] = [opt]

        opt = self.config['blog_default_location']
        if opt is not None and not isinstance(opt, list):
            self.config['blog_default_location'] = [opt]

        self.blog = Catalog(self, 'blog', 'blog', None)
        self.archive = Catalog(self, 'archive', 'archive', None)

        self.catalogs = cat = {}  # catalogs of users set labels
        self.tags = cat['tags'] = Catalog(self, 'tags', 'tag', 'tag')
        self.author = cat['author'] = Catalog(self, 'author',
            'author', 'author')
        self.location = cat['location'] = Catalog(self, 'location',
            'location',  'location')
        self.category = cat['category'] = Catalog(self, 'category',
            'category', 'category')

        for catname in ['author', 'location']:
            catalog = self.catalogs[catname]
            items = self.config['blog_' + catname + 's'].items()
            for label, (name, link) in items:
                catalog[label] = Collection(catalog, label, name, link)


        self.posts = self.blog['post'] = Collection(self.blog, 'post',
            'Posts', path=self.blog_path)
        self.drafts = self.blog['draft'] = Collection(self.blog, 'draft',
            'Drafts', path=os.path.join(self.blog_path, 'drafts'))
        # add references to posts and drafts
        # e.g. :ref:`blog-posts`
        domain = self.app.env.domains['std']
        domain.data['labels']['blog-posts'] = (
            os.path.join(self.config['blog_path'], 'index'), '', 'Posts')
        domain.data['labels']['blog-drafts'] = (
            os.path.join(self.config['blog_path'], 'drafts', 'index'), '',
                         'Drafts')
        domain.data['labels']['blog-feed'] = (
            os.path.join(self.config['blog_path'], 'atom.xml'), '',
            self.blog_title + ' Feed')

        self.config['cloud_size'] = 5
        self.config['fontawesome'] = (self.config['fontawesome_included'] or
                                      self.config['fontawesome_link_cdn'] or
                                      self.config['fontawesome_css_file'])

    def __getattr__(self, name):

        try:
            attr = self.config[name]
        except KeyError:
            raise AttributeError('ABlog has no configuration option {}'
                                 .format(repr(name)))
        return attr

    def __getitem__(self, key):

        return self.posts[key] or self.drafts[key]

    def __contains__(self, item):

        return item in self.posts or item in self.drafts

    def __len__(self):

        return len(self.posts)

    def __nonzero__(self):

        return len(self) > 0

    @property
    def feed_path(self):
        """RSS feed page name."""

        return os.path.join(self.blog_path, 'rss.xml')

    def register(self, docname, info):
        """Register post *docname*."""


        post = Post(self, docname, info)
        if post.date and post.date < TOMORROW:
            self.posts.add(post)
        else:
            self.drafts.add(post)
        for catalog in self.catalogs.values():
            catalog.add(post)

    def recent(self, num, docname=None, **labels):
        """Yield *num* recent posts, excluding the one with `docname`."""

        for i, post in enumerate(self.posts):
            if post.docname == docname:
                num += 1
                continue
            if i == num:
                return
            yield post

    def link_posts(self):
        """Link posts after sorting them post by published date."""

        posts = list(self.posts)
        posts.sort()
        posts[0].prev = posts[-1].next = None
        for i in range(1, len(posts)):
            post = posts[i]
            posts[i - 1].next = post
            post.prev = posts[i - 1]


def html_builder_write_doc(self, docname, doctree):
    """Part of :meth:`sphinx.builders.html.StandaloneHTMLBuilder.write_doc`
    method used to convert *doctree* to HTML."""

    destination = StringOutput(encoding='utf-8')
    doctree.settings = self.docsettings

    self.secnumbers = {}
    self.imgpath = relative_uri(self.get_target_uri(docname), '_images')
    self.dlpath = relative_uri(self.get_target_uri(docname), '_downloads')
    self.current_docname = docname
    self.docwriter.write(doctree, destination)
    self.docwriter.assemble_parts()
    return self.docwriter.parts['fragment']


class Post(object):

    """Handle post metadata."""

    def __init__(self, ablog, docname, info):


        self.ablog = ablog
        self.docname = docname
        self.date = date = info['date']
        self.update = info['update']
        self.published = date and date < TOMORROW
        self.draft = not self.published
        self.title = info['title']
        self.excerpt = info['excerpt']
        self._next = self._prev = -1

        #self.language = info.get('language')

        # archives
        self.blog = []
        if self.published:
            self.tags = info.get('tags')
            self.author = info.get('author')
            self.category = info.get('category')
            self.location = info.get('location')

            if not self.author and ablog.blog_default_author:
                self.author = ablog.blog_default_author
            if not self.location and ablog.blog_default_location:
                self.location = ablog.blog_default_location

            self.archive = self.ablog.archive[self.date.year]
            self.archive.add(self)

        else:
            self.tags = info.get('tags')
            self.author = info.get('author')
            self.category = info.get('category')
            self.location = info.get('location')
            self.archive = []

        self.redirect = info.get('redirect')

        self.options = info

    def __lt__(self, other):

        return (self.date or FUTURE) < (other.date or FUTURE)

    def summary(self, pagename):
        """Return summary after resolving references with respect to
        *pagename*."""

        doctree = nodes.document({}, dummy_reporter)
        for node in self.excerpt:
            doctree.append(node.deepcopy())
        app = self.ablog.app
        app.env.resolve_references(doctree, pagename, app.builder)
        return html_builder_write_doc(app.builder, pagename, doctree)

    def _summarize(self, doctree, npars, image):
        """Create a summary of the post."""

        p_count = 0
        i = 0
        title_visited = False
        doctree = doctree.deepcopy()
        remove = []
        for node in doctree.traverse():
            if isinstance(node, nodes.title) and not title_visited:
                title_visited = True
                remove.append(node)
                continue
            if isinstance(node, nodes.paragraph):
                p_count += 1
            if isinstance(node, (nodes.image, nodes.figure)):
                i += 1
                if i != image:
                    remove.append(node)
            elif p_count >= npars:
                remove.append(node)
        for node in remove:
            node.parent.remove(node)

        self._summary = doctree

    @property
    def next(self):
        """Next published post in chronological order."""

        if self._next == -1:
            self.ablog.link_posts()
        return self._next

    @next.setter
    def next(self, post):
        """Set next published post in chronological order."""

        self._next = post

    @property
    def prev(self):
        """Previous published post in chronological order."""

        if self._prev == -1:
            self.ablog.link_posts()
        return self._prev

    @prev.setter
    def prev(self, post):
        """Set previous published post in chronological order."""

        self._prev = post


class Catalog(object):

    """Handles collections of posts."""

    def __init__(self, blog, name, xref, path):

        self.blog = blog
        self.name = name
        self.xref = xref # for creating labels, e.g. `tag-python`
        self.collections = {}

        if path:
            self.path = self.docname = os.path.join(blog.blog_path, path)
        else:
            self.path = self.docname = blog.blog_path

        self._lens = None
        self._minmax = None

    def __getitem__(self, name):

        try:
            return self.collections[name]
        except KeyError:
            return self.collections.setdefault(name, Collection(self, name))

    def __setitem__(self, name, item):

        self.collections[name] = item

    def __len__(self):

        return sum(len(coll) for coll in self)

    def __nonzero__(self):

        return len(self) > 0

    def __iter__(self):

        keys = list(self.collections)
        keys.sort()
        for key in keys:
            yield self.collections[key]

    def add(self, post):
        """Add post to appropriate collection(s) and replace collections
        labels with collection objects."""

        colls = []
        for label in getattr(post, self.name, []):
            coll = self[label]
            if post.published:
                coll.add(post)
            colls.append(coll)
        setattr(post, self.name, colls)

    def minmax(self):
        """Return minimum and maximum sizes of collections."""

        if self._lens is None or len(self._lens) != len(self.collections):
            self._lens = [len(coll) for coll in self.collections.values()
                          if len(coll)]
            self._minmax = min(self._lens), max(self._lens)
        return self._minmax


class Collection(object):

    """Posts sharing a label, i.e. tag, category, author, or location."""

    def __init__(self, catalog, label, name=None, href=None, path=None):

        self.catalog = catalog
        self.label = label
        self.name = name or self.label
        self.href = href

        self._posts = {}

        self._path = path
        self.xref = self.catalog.xref + '-' + slugify(label)
        self._slug = None
        self._html = None

        self.catalog.blog.std_domain.data['labels'][self.xref] = (
            self.docname, self.xref, self.name)

    def __str__(self):

        return str(self.name)

    def __len__(self):

        return len(self._posts)

    def __nonzero__(self):

        return len(self) > 0

    def __unicode__(self):

        return unicode(self.name)

    def __iter__(self):

        posts = list(self._posts.values())
        posts.sort(reverse=True)
        for post in posts:
            yield post

    def __getitem__(self, key):

        return self._posts.get(key)

    def __contains__(self, item):

        return item in self._posts

    def add(self, post):
        """Add post to the collection."""

        self._posts[post.docname] = post

    @property
    def relsize(self):
        """Relative size used in tag clouds. Relat"""

        if len(self.catalog) == 1:
            return 3
        min_, max_ = self.catalog.minmax()
        size = int((len(self) - min_) / max(max_ - min_, 1) *
                   (self.catalog.blog.cloud_size - 1)) + 1
        return size

    @property
    def docname(self):
        """Collection page document name."""

        if self._path is None:
            self._path = os.path.join(self.catalog.path, slugify(self.name))
        return self._path
