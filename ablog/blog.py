"""
Classes for handling posts and archives.
"""

import os
import re
import datetime as dtmod
from datetime import datetime
from unicodedata import normalize
from urllib.parse import urljoin
from collections.abc import Container

from docutils import nodes
from docutils.io import StringOutput
from docutils.utils import new_document
from sphinx import addnodes
from sphinx.util.osutil import relative_uri

__all__ = ["Blog", "Post", "Collection"]


def slugify(string):
    """
    Slugify *s*.
    """

    string = normalize("NFKD", str(string))
    string = re.sub(r"[^\w\s-]", "", string).strip().lower()
    return re.sub(r"[-\s]+", "-", string)


def os_path_join(path, *paths):

    return os.path.join(path, *paths).replace(os.path.sep, "/")


def require_config_type(type_, is_optional=True):
    def verify_fn(key, value, config):
        if isinstance(value, type_) or (is_optional and value is None):
            return value
        # Historically, we're pretty sloppy on whether None or False is the default for omission
        # so accept them both.
        if value is False and is_optional:
            return None
        raise KeyError(key + " must be a " + type_.__name__ + (" or omitted" if is_optional else ""))

    return verify_fn


def require_config_str_or_list_lookup(lookup_config_key, is_optional=True):
    """
    The default values can be a string or list of strings that match entries in
    a comprehensive list -- for example, the default authors are one or more of
    all the authors.
    """

    def verify_fn(key, value, config):
        if is_optional and value is None:
            return value
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            raise KeyError(key + " must be a str or list")

        allowed_values = config[lookup_config_key]
        for v in value:
            if v not in allowed_values:
                raise KeyError(str(v) + "must be a key of " + lookup_config_key)
        return value

    return verify_fn


def require_config_full_name_link_dict(is_link_optional=True):
    """
    The definition for authors and similar entries is to map a short name to a
    (full name, link) tuple.
    """

    def verify_fn(key, value, config):
        for full_name, link in value.values():
            if not isinstance(full_name, str):
                raise KeyError(key + " must have full name entries that are strings")
            is_link_valid = isinstance(link, str) or (is_link_optional and link is None)
            if not is_link_valid:
                raise KeyError(key + " links must be a string" + (" or omitted" if is_link_optional else ""))
        return value

    return verify_fn


DEBUG = True
CONFIG = [
    # name, default, rebuild, verify_fn
    # where verify_fn is (key, value, app.config) --> value, throwing a KeyError if the value isn't right
    ("blog_path", "blog", True, require_config_type(str)),
    ("blog_title", "Blog", True, require_config_type(str)),
    ("blog_baseurl", "", True, require_config_type(str)),
    ("blog_archive_titles", None, False, require_config_type(bool)),
    ("blog_feed_archives", False, True),
    ("blog_feed_fulltext", False, True),
    ("blog_feed_subtitle", None, True),
    ("blog_feed_titles", None, False),
    ("blog_feed_length", None, None),
    ("blog_authors", {}, True, require_config_full_name_link_dict()),
    ("blog_default_author", None, True, require_config_str_or_list_lookup("blog_authors")),
    ("blog_locations", {}, True, require_config_full_name_link_dict()),
    ("blog_default_location", None, True, require_config_str_or_list_lookup("blog_locations")),
    ("blog_languages", {}, True, require_config_full_name_link_dict()),
    ("blog_default_language", None, True, require_config_str_or_list_lookup("blog_languages")),
    ("fontawesome_link_cdn", None, True),
    ("fontawesome_included", False, True, require_config_type(bool)),
    ("fontawesome_css_file", "", True, require_config_type(str)),
    ("post_date_format", "%d %B %Y", True, require_config_type(str)),
    ("post_date_format_short", "%d %B", True, require_config_type(str)),
    ("post_auto_orphan", True, True, require_config_type(bool)),
    ("post_auto_image", 0, True),
    ("post_auto_excerpt", 1, True),
    ("post_redirect_refresh", 5, True),
    ("post_always_section", False, True),
    ("disqus_shortname", None, True),
    ("disqus_drafts", False, True),
    ("disqus_pages", False, True),
    ("blog_post_pattern", "", True, require_config_type(str)),
]


TOMORROW = datetime.today() + dtmod.timedelta(1)
TOMORROW = TOMORROW.replace(hour=0, minute=0, second=0, microsecond=0)
FUTURE = datetime(9999, 12, 31)


def revise_pending_xrefs(doctree, docname):

    for node in doctree.traverse(addnodes.pending_xref):
        node["refdoc"] = docname


def link_posts(posts):
    """
    Link posts after sorting them post by published date.
    """

    from operator import attrgetter

    posts = filter(attrgetter("order"), posts)
    posts = sorted(posts)
    posts[0].prev = posts[-1].next = None
    for i in range(1, len(posts)):
        post = posts[i]
        posts[i - 1].next = post
        post.prev = posts[i - 1]


class Blog(Container):

    """
    Handle blog operations.
    """

    # using a shared state
    _dict = {}

    def __init__(self, app):

        self.__dict__ = self._dict
        if not self._dict:
            self._init(app)

    def _init(self, app):
        """
        Instantiate Blog.
        """

        self.app = app
        self.config = {}

        self.references = refs = {}

        # get configuration from Sphinx app
        for opt in CONFIG:
            try:
                key, _, _, verify_fn = opt
            except ValueError:
                key, _, _ = opt
                verify_fn = None
            value = (
                verify_fn(key, getattr(app.config, key), app.config)
                if verify_fn
                else getattr(app.config, opt[0])
            )
            self.config[opt[0]] = value

        # blog catalog contains all posts
        self.blog = Catalog(self, "blog", "blog", None)

        # contains post collections by year
        self.archive = Catalog(self, "archive", "archive", None, reverse=True)
        self.archive.docname += "/archive"
        refs["blog-archives"] = (self.archive.docname, "Archives")

        self.catalogs = cat = {}  # catalogs of user set labels
        self.tags = cat["tags"] = Catalog(self, "tags", "tag", "tag")
        refs["blog-tags"] = (self.tags.docname, "Tags")

        self.author = cat["author"] = Catalog(self, "author", "author", "author")
        refs["blog-authors"] = (self.author.docname, "Authors")

        self.location = cat["location"] = Catalog(self, "location", "location", "location")
        refs["blog-locations"] = (self.location.docname, "Locations")

        self.language = cat["language"] = Catalog(self, "language", "language", "language")
        refs["blog-languages"] = (self.language.docname, "Languages")

        self.category = cat["category"] = Catalog(self, "category", "category", "category")
        refs["blog-categories"] = (self.category.docname, "Categories")

        for catname in ["author", "location", "language"]:
            catalog = self.catalogs[catname]
            items = self.config["blog_" + catname + "s"].items()
            for label, (name, link) in items:
                catalog[label] = Collection(catalog, label, name, link)

        self.posts = self.blog["post"] = Collection(self.blog, "post", "Posts", path=self.blog_path)
        self.drafts = self.blog["draft"] = Collection(
            self.blog, "draft", "Drafts", path=os_path_join(self.blog_path, "drafts")
        )

        # add references to posts and drafts
        # e.g. :ref:`blog-posts`
        refs["blog-posts"] = (os_path_join(self.config["blog_path"], "index"), "Posts")
        refs["blog-drafts"] = (os_path_join(self.config["blog_path"], "drafts", "index"), "Drafts")
        refs["blog-feed"] = (os_path_join(self.config["blog_path"], "atom.xml"), self.blog_title + " Feed")

        # set some internal configuration options
        self.config["fontawesome"] = (
            self.config["fontawesome_included"]
            or self.config["fontawesome_link_cdn"]
            or self.config["fontawesome_css_file"]
        )

    def __getattr__(self, name):

        try:
            attr = self.config[name]
        except KeyError:
            raise AttributeError("ABlog has no configuration option {}".format(repr(name)))
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
        """
        RSS feed page name.
        """

        return os_path_join(self.blog_path, "atom.xml")

    def register(self, docname, info):
        """
        Register post *docname*.
        """

        post = Post(self, docname, info)
        if post.date and post.date < TOMORROW:
            self.posts.add(post)
        else:
            self.drafts.add(post)
        for catalog in self.catalogs.values():
            catalog.add(post)

    def recent(self, num, docname=None, **labels):
        """
        Yield *num* recent posts, excluding the one with `docname`.
        """

        if num is None:
            num = len(self)
        for i, post in enumerate(self.posts):
            if post.docname == docname:
                num += 1
                continue
            if i == num:
                return
            yield post

    def page_id(self, pagename):
        """
        Return pagename, trimming :file:`index` from end when found.

        Return value is used as disqus page identifier.
        """

        if self.config["blog_baseurl"]:
            if pagename.endswith("index"):
                pagename = pagename[:-5]
            pagename = pagename.strip("/")
            return "/" + pagename + ("/" if pagename else "")

    def page_url(self, pagename):
        """
        Return page URL when :confval:`blog_baseurl` is set, otherwise
        ``None``.

        When found, :file:`index.html` is trimmed from the end of the
        URL.
        """

        if self.config["blog_baseurl"]:
            url = urljoin(self.config["blog_baseurl"], pagename)
            if url.endswith("index"):
                url = url[:-5]
            return url


def html_builder_write_doc(self, docname, doctree):
    """
    Part of :meth:`sphinx.builders.html.StandaloneHTMLBuilder.write_doc` method
    used to convert *doctree* to HTML.
    """

    destination = StringOutput(encoding="utf-8")
    doctree.settings = self.docsettings

    self.secnumbers = {}
    self.imgpath = relative_uri(self.get_target_uri(docname), "_images")
    self.dlpath = relative_uri(self.get_target_uri(docname), "_downloads")
    self.current_docname = docname
    self.docwriter.write(doctree, destination)
    self.docwriter.assemble_parts()
    return self.docwriter.parts["fragment"]


class BlogPageMixin:
    def __str__(self):
        return self.title

    def __repr__(self):

        return str(self) + " <" + str(self.docname) + ">"

    @property
    def blog(self):
        """
        Reference to :class:`~ablog.blog.Blog` object.
        """

        return self._blog

    @property
    def title(self):

        return getattr(self, "name", getattr(self, "_title"))


class Post(BlogPageMixin):

    """
    Handle post metadata.
    """

    def __init__(self, blog, docname, info):

        self._blog = blog
        self.docname = docname
        self.section = info["section"]
        self.order = info["order"]
        self.date = date = info["date"]
        self.update = info["update"]
        self.nocomments = info["nocomments"]
        self.published = date and date < TOMORROW
        self.draft = not self.published
        self._title = info["title"]
        self.excerpt = info["excerpt"]
        self.doctree = info["doctree"]
        self._next = self._prev = -1
        self._computed_date = date or FUTURE

        # self.language = info.get('language')

        # archives
        # self.blog = []
        if self.published:
            self.tags = info.get("tags")
            self.author = info.get("author")
            self.category = info.get("category")
            self.location = info.get("location")
            self.language = info.get("language")

            if not self.author and blog.blog_default_author:
                self.author = blog.blog_default_author
            if not self.location and blog.blog_default_location:
                self.location = blog.blog_default_location
            if not self.language and blog.blog_default_language:
                self.language = blog.blog_default_language

            self.archive = self._blog.archive[self.date.year]
            self.archive.add(self)

        else:
            self.tags = info.get("tags")
            self.author = info.get("author")
            self.category = info.get("category")
            self.location = info.get("location")
            self.language = info.get("language")
            self.archive = []

        self.redirect = info.get("redirect")

        self.options = info

    def __lt__(self, other):
        return (self._computed_date, self.title) < (other._computed_date, other.title)

    def to_html(self, pagename, fulltext=False, drop_h1=True):
        """
        Return excerpt or *fulltext* as HTML after resolving references with
        respect to *pagename*.

        By default, first `<h1>` tag is dropped from the output. More
        than one can be dropped by setting *drop_h1* to the desired
        number of tags to be dropped.
        """

        doctree = new_document("")
        if fulltext:
            deepcopy = self.doctree.deepcopy()
            if isinstance(deepcopy, nodes.document):
                doctree.extend(deepcopy.children)
            else:
                doctree.append(deepcopy)
        else:
            for node in self.excerpt:
                doctree.append(node.deepcopy())
        app = self._blog.app

        revise_pending_xrefs(doctree, pagename)
        app.env.resolve_references(doctree, pagename, app.builder)

        add_permalinks, app.builder.add_permalinks = (app.builder.add_permalinks, False)

        html = html_builder_write_doc(app.builder, pagename, doctree)

        app.builder.add_permalinks = add_permalinks

        if drop_h1:
            html = re.sub("<h1>(.*?)</h1>", "", html, count=abs(int(drop_h1)))
        return html

    @property
    def next(self):
        """
        Next published post in chronological order.
        """

        if self._next == -1:
            link_posts(self._blog.posts)
        return self._next

    @next.setter
    def next(self, post):
        """
        Set next published post in chronological order.
        """

        self._next = post

    @property
    def prev(self):
        """
        Previous published post in chronological order.
        """

        if self._prev == -1:
            link_posts(self._blog.posts)
        return self._prev

    @prev.setter
    def prev(self, post):
        """
        Set previous published post in chronological order.
        """

        self._prev = post


class Catalog(BlogPageMixin):

    """
    Handles collections of posts.
    """

    def __init__(self, blog, name, xref, path, reverse=False):

        self._blog = blog
        self.name = name
        self.xref = xref  # for creating labels, e.g. `tag-python`
        self.collections = {}

        if path:
            self.path = self.docname = os_path_join(blog.blog_path, path)
        else:
            self.path = self.docname = blog.blog_path

        self._coll_lens = None
        self._min_max = None
        self._reverse = reverse

    def __str__(self):

        return str(self.name)

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
        keys.sort(reverse=self._reverse)
        for key in keys:
            yield self.collections[key]

    def add(self, post):
        """
        Add post to appropriate collection(s) and replace collections labels
        with collection objects.
        """

        colls = []
        for label in getattr(post, self.name, []):
            coll = self[label]
            if post.published:
                coll.add(post)
            colls.append(coll)
        setattr(post, self.name, colls)

    def _minmax(self):
        """
        Return minimum and maximum sizes of collections.
        """

        if self._coll_lens is None or len(self._coll_lens) != len(self.collections):
            self._coll_lens = [len(coll) for coll in self.collections.values() if len(coll)]
            self._min_max = min(self._coll_lens), max(self._coll_lens)
        return self._min_max


class Collection(BlogPageMixin):

    """
    Posts sharing a label, i.e. tag, category, author, or location.
    """

    def __init__(self, catalog, label, name=None, href=None, path=None, page=0):

        self._catalog = catalog
        self._blog = catalog.blog
        self.label = label
        self.name = name or self.label
        self.href = href
        self.page = page
        self._posts = {}
        self._posts_iter = None
        self._path = path
        self.xref = self.catalog.xref + "-" + slugify(label)
        self._slug = None
        self._html = None

        self._catalog.blog.references[self.xref] = (self.docname, self.name)

    def __str__(self):

        return str(self.name)

    def __len__(self):

        return len(self._posts)

    def __nonzero__(self):

        return len(self) > 0

    def __unicode__(self):

        return str(self.name)

    def __iter__(self):

        if self._posts_iter is None:
            posts = list(self._posts.values())
            posts.sort(reverse=True)
            self._posts_iter = posts

        yield from self._posts_iter

    def __getitem__(self, key):

        return self._posts.get(key)

    def __contains__(self, item):

        return item in self._posts

    @property
    def catalog(self):
        """
        :class:`~ablog.blog.Catalog` that the collection belongs to.
        """

        return self._catalog

    def add(self, post):
        """
        Add post to the collection.
        """

        post_name = post.docname
        if post.section:
            post_name += "#" + post.section
        self._posts[post_name] = post

    def relsize(self, maxsize=5, minsize=1):
        """
        Relative size used in tag clouds.
        """

        min_, max_ = self.catalog._minmax()

        diff = maxsize - minsize
        if len(self.catalog) == 1 or min_ == max_:
            return int(round(diff / 2.0 + minsize))

        size = int(1.0 * (len(self) - min_) / (max_ - min_) * diff + minsize)
        return size

    @property
    def docname(self):
        """
        Collection page document name.
        """

        if self._path is None:
            self._path = os_path_join(self.catalog.path, slugify(self.name))
        return self._path

    path = docname
