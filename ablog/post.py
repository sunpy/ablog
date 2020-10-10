"""
post and postlist directives.
"""
import os
import logging
from string import Formatter
from datetime import datetime

from dateutil.parser import parse as date_parser
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from feedgen.feed import FeedGenerator
from sphinx.locale import _
from sphinx.transforms import SphinxTransform
from sphinx.util.nodes import set_source_info

import ablog

from .blog import Blog, os_path_join, revise_pending_xrefs, slugify

text_type = str

__all__ = [
    "PostNode",
    "PostList",
    "UpdateNode",
    "PostDirective",
    "UpdateDirective",
    "PostListDirective",
    "CheckFrontMatter",
    "purge_posts",
    "process_posts",
    "process_postlist",
    "generate_archive_pages",
    "generate_atom_feeds",
    "register_posts",
]


class PostNode(nodes.Element):
    """
    Represent ``post`` directive content and options in document tree.
    """


class PostList(nodes.General, nodes.Element):
    """
    Represent ``postlist`` directive converted to a list of links.
    """


class UpdateNode(nodes.admonition):
    """
    Represent ``update`` directive.
    """


class PostDirective(Directive):
    """
    Handle ``post`` directives.
    """

    def _split(a):  # NOQA
        return [s.strip() for s in (a or "").split(",") if s.strip()]

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "tags": _split,
        "author": _split,
        "category": _split,
        "location": _split,
        "language": _split,
        "redirect": _split,
        "title": lambda a: a.strip(),
        "image": int,
        "excerpt": int,
        "exclude": directives.flag,
        "nocomments": directives.flag,
    }

    def run(self):

        node = PostNode()
        node.document = self.state.document
        set_source_info(self, node)
        self.state.nested_parse(self.content, self.content_offset, node, match_titles=1)

        node = _update_post_node(node, self.options, self.arguments)
        return [node]


class UpdateDirective(BaseAdmonition):
    required_arguments = 1
    node_class = UpdateNode

    def run(self):
        ad = super().run()
        ad[0]["date"] = self.arguments[0] if self.arguments else ""
        return ad


class PostListDirective(Directive):
    """
    Handle ``postlist`` directives.
    """

    def _split(a):  # NOQA
        return {s.strip() for s in a.split(",")}

    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        "tags": _split,
        "author": _split,
        "category": _split,
        "location": _split,
        "language": _split,
        "format": lambda a: a.strip(),
        "date": lambda a: a.strip(),
        "sort": directives.flag,
        "excerpts": directives.flag,
        "list-style": lambda a: a.strip(),
    }

    def run(self):

        node = PostList()
        node.document = self.state.document
        set_source_info(self, node)
        self.state.nested_parse(self.content, self.content_offset, node, match_titles=1)

        node["length"] = int(self.arguments[0]) if self.arguments else None
        node["tags"] = self.options.get("tags", [])
        node["author"] = self.options.get("author", [])
        node["category"] = self.options.get("category", [])
        node["location"] = self.options.get("location", [])
        node["language"] = self.options.get("language", [])
        node["format"] = self.options.get("format", "{date} - {title}")
        node["date"] = self.options.get("date", None)
        node["sort"] = "sort" in self.options
        node["excerpts"] = "excerpts" in self.options
        node["image"] = "image" in self.options
        node["list-style"] = self.options.get("list-style", "none")
        return [node]


class CheckFrontMatter(SphinxTransform):
    """
    Check the doctree for frontmatter meant for a blog post.

    This is mutually-exclusive with the PostDirective. Only one much be
    used.
    """

    # Priority before 880 so that it runs before the `doctree-read` event
    default_priority = 800

    def apply(self):
        # Check if page-level metadata has been given
        docinfo = list(self.document.traverse(nodes.docinfo))
        if not docinfo:
            return None
        docinfo = docinfo[0]

        # Pull the metadata for the page to check if it is a blog post
        metadata = {fn.children[0].astext(): fn.children[1].astext() for fn in docinfo.traverse(nodes.field)}
        if docinfo.traverse(nodes.author):
            metadata["author"] = list(docinfo.traverse(nodes.author))[0].astext()
        # These two fields are special-cased in docutils
        if docinfo.traverse(nodes.date):
            metadata["date"] = list(docinfo.traverse(nodes.date))[0].astext()
        if "blogpost" not in metadata and self.env.docname not in self.config.matched_blog_posts:
            return None
        if self.document.traverse(PostNode):
            logging.warning(f"Found blog post front-matter as well as post directive, using post directive.")

        # Iterate through metadata and create a PostNode with relevant fields
        option_spec = PostDirective.option_spec
        for key, val in metadata.items():
            if key in option_spec:
                if callable(option_spec[key]):
                    new_val = option_spec[key](val)
                elif isinstance(option_spec[key], directives.flag):
                    new_val = True
                metadata[key] = new_val

        node = PostNode()
        node.document = self.document
        node = _update_post_node(node, metadata, [])
        node["date"] = metadata.get("date")

        if not metadata.get("excerpt"):
            blog = Blog(self.app)
            node["excerpt"] = blog.post_auto_excerpt

        sections = list(self.document.traverse(nodes.section))
        if sections:
            sections[0].children.append(node)
            node.parent = sections[0]


def purge_posts(app, env, docname):
    """
    Remove post and reference to it from the standard domain when its document
    is removed or changed.
    """

    if hasattr(env, "ablog_posts"):
        env.ablog_posts.pop(docname, None)

    filename = os.path.split(docname)[1]
    env.domains["std"].data["labels"].pop(filename, None)
    env.domains["std"].data["anonlabels"].pop(filename, None)


def _update_post_node(node, options, arguments):
    """
    Extract metadata from options and populate a post node.
    """
    node["date"] = arguments[0] if arguments else None
    node["tags"] = options.get("tags", [])
    node["author"] = options.get("author", [])
    node["category"] = options.get("category", [])
    node["location"] = options.get("location", [])
    node["language"] = options.get("language", [])
    node["redirect"] = options.get("redirect", [])
    node["title"] = options.get("title", None)
    node["image"] = options.get("image", None)
    node["excerpt"] = options.get("excerpt", None)
    node["exclude"] = "exclude" in options
    node["nocomments"] = "nocomments" in options
    return node


def _get_section_title(section):
    """
    Return section title as text.
    """

    for title in section.traverse(nodes.title):
        return title.astext()
    raise Exception("Missing title")
    # A problem with the following is that title may contain pending
    # references, e.g. :ref:`tag-tips`


def _get_update_dates(section, docname, post_date_format):
    """
    Return list of dates of updates found section.
    """

    update_nodes = list(section.traverse(UpdateNode))
    update_dates = []
    for update_node in update_nodes:
        try:
            update = datetime.strptime(update_node["date"], post_date_format)
        except ValueError:
            if date_parser:
                try:
                    update = date_parser(update_node["date"])
                except ValueError:
                    raise ValueError("invalid post date in: " + docname)
            else:
                raise ValueError(
                    f"invalid post date ({update_node['date']}) in "
                    + docname
                    + f". Expected format: {post_date_format}"
                )
        # Insert a new title element which contains the `Updated on {date}` logic.
        substitute = nodes.title("", "Updated on " + update.strftime(post_date_format))
        update_node.insert(0, substitute)
        update_node["classes"] = ["note", "update"]

        update_dates.append(update)
    return update_dates


def process_posts(app, doctree):
    """
    Process posts and map posted document names to post details in the
    environment.
    """

    env = app.builder.env
    if not hasattr(env, "ablog_posts"):
        env.ablog_posts = {}

    post_nodes = list(doctree.traverse(PostNode))
    if not post_nodes:
        return
    post_date_format = app.config["post_date_format"]
    should_auto_orphan = app.config["post_auto_orphan"]
    docname = env.docname

    if should_auto_orphan:
        # mark the post as 'orphan' so that
        #   "document isn't included in any toctree" warning is not issued
        # We do not simply assign to should_auto_orphan because if auto-orphan
        # is false, we still want to respect the per-post :rst:dir`orphan` setting
        app.env.metadata[docname]["orphan"] = True

    blog = Blog(app)
    auto_excerpt = blog.post_auto_excerpt
    multi_post = len(post_nodes) > 1 or blog.post_always_section

    for order, node in enumerate(post_nodes, start=1):
        if node["excerpt"] is None:
            node["excerpt"] = auto_excerpt

        if multi_post:
            # section title, and first few paragraphs of the section of post
            # are used when there are more than 1 posts
            section = node
            while True:
                if isinstance(section, nodes.section):
                    break
                section = node.parent
        else:
            section = doctree

        # get updates here, in the section that post belongs to
        # Might there be orphan updates?
        update_dates = _get_update_dates(section, docname, post_date_format)

        # Making sure that post has a title because all post titles
        # are needed when resolving post lists in documents
        title = node["title"] or _get_section_title(section)

        # creating a summary here, before references are resolved
        excerpt = []
        if node.children:
            if node["exclude"]:
                node.replace_self([])
            else:
                node.replace_self(node.children)
            for child in node.children:
                excerpt.append(child.deepcopy())
        elif node["excerpt"]:
            count = 0
            for nod in section.traverse(nodes.paragraph):
                excerpt.append(nod.deepcopy())
                count += 1
                if count >= (node["excerpt"] or 0):
                    break
            node.replace_self([])
        else:
            node.replace_self([])
        nimg = node["image"] or blog.post_auto_image
        if nimg:
            for img, nod in enumerate(section.traverse(nodes.image), start=1):
                if img == nimg:
                    excerpt.append(nod.deepcopy())
                    break
        date = node["date"]
        if date:
            try:
                date = datetime.strptime(date, post_date_format)
            except ValueError:
                if date_parser:
                    try:
                        date = date_parser(date)
                    except ValueError:
                        raise ValueError("invalid post date in: " + docname)
                else:
                    raise ValueError(
                        "invalid post date (%s) in " % (date)
                        + docname
                        + ". Expected format: %s" % post_date_format
                    )

        else:
            date = None

        # if docname ends with `index` use folder name to reference the document
        # a potential problem here is that there may be files/folders with the
        #   same name, so issuing a warning when that's the case may be a good idea
        folder, label = os.path.split(docname)
        if label == "index":
            folder, label = os.path.split(folder)
        if not label:
            label = slugify(title)

        section_name = ""
        if multi_post and section.parent is not doctree:
            section_name = section.attributes["ids"][0]
            label += "-" + section_name
        else:
            # create a reference for the post
            # if it is posting the document
            # ! this does not work for sections
            app.env.domains["std"].data["labels"][label] = (docname, label, title)
            app.env.domains["std"].data["anonlabels"][label] = (docname, label)

        if section.parent is doctree:
            section_copy = section[0].deepcopy()
        else:
            section_copy = section.deepcopy()

        # multiple posting may result having post nodes
        for nn in section_copy.traverse(PostNode):
            if nn["exclude"]:
                nn.replace_self([])
            else:
                nn.replace_self(node.children)

        postinfo = {
            "docname": docname,
            "section": section_name,
            "order": order,
            "date": date,
            "update": max(update_dates + [date]),
            "title": title,
            "excerpt": excerpt,
            "tags": node["tags"],
            "author": node["author"],
            "category": node["category"],
            "location": node["location"],
            "language": node["language"],
            "redirect": node["redirect"],
            "nocomments": node["nocomments"],
            "image": node["image"],
            "exclude": node["exclude"],
            "doctree": section_copy,
        }

        if docname not in env.ablog_posts:
            env.ablog_posts[docname] = []
        env.ablog_posts[docname].append(postinfo)

        # instantiate catalogs and collections here
        #  so that references are created and no warnings are issued
        if app.builder.format == "html":
            stdlabel = env.domains["std"].data["labels"]  # NOQA
        else:
            stdlabel = env.intersphinx_inventory.setdefault("std:label", {})  # NOQA
            baseurl = getattr(env.config, "blog_baseurl").rstrip("/") + "/"  # NOQA
            project, version = env.config.project, text_type(env.config.version)  # NOQA

        for key in ["tags", "author", "category", "location", "language"]:
            catalog = blog.catalogs[key]
            for label in postinfo[key]:
                coll = catalog[label]  # NOQA

        if postinfo["date"]:
            coll = blog.archive[postinfo["date"].year]  # NOQA


def process_postlist(app, doctree, docname):
    """
    Replace `PostList` nodes with lists of posts.

    Also, register all posts if they have not been registered yet.
    """

    blog = Blog(app)
    if not blog:
        register_posts(app)

    for node in doctree.traverse(PostList):
        colls = []
        for cat in ["tags", "author", "category", "location", "language"]:
            for coll in node[cat]:
                if coll in blog.catalogs[cat].collections:
                    colls.append(blog.catalogs[cat].collections[coll])

        if colls:
            posts = set(blog.posts)
            for coll in colls:
                posts = posts & set(coll)
            posts = list(posts)
            posts.sort(reverse=True)
            posts = posts[: node.attributes["length"]]
        else:
            posts = list(blog.recent(node.attributes["length"], docname, **node.attributes))

        if node.attributes["sort"]:
            posts.sort()  # in reverse chronological order, so no reverse=True

        fmts = list(Formatter().parse(node.attributes["format"]))
        not_in = {"date", "title", "author", "location", "language", "category", "tags", None}
        for text, key, __, __ in fmts:
            if key not in not_in:
                raise KeyError(f"{key} is not recognized in postlist format")

        excerpts = node.attributes["excerpts"]
        date_format = node.attributes["date"] or _(blog.post_date_format_short)
        bl = nodes.bullet_list()
        bl.attributes["classes"].append("postlist-style-" + node["list-style"])
        bl.attributes["classes"].append("postlist")
        for post in posts:
            bli = nodes.list_item()
            bl.append(bli)
            par = nodes.paragraph()
            bli.append(par)

            for text, key, __, __ in fmts:
                if text:
                    par.append(nodes.Text(text))
                if key is None:
                    continue
                if key == "date":
                    par.append(nodes.Text(post.date.strftime(date_format)))
                else:
                    if key == "title":
                        items = [post]
                    else:
                        items = getattr(post, key)

                    for i, item in enumerate(items, start=1):
                        if key == "title":
                            ref = nodes.reference()
                            ref["refuri"] = app.builder.get_relative_uri(docname, item.docname)
                            ref["ids"] = []
                            ref["backrefs"] = []
                            ref["dupnames"] = []
                            ref["classes"] = []
                            ref["names"] = []
                            ref["internal"] = True
                            ref.append(nodes.Text(text_type(item)))
                        else:
                            ref = _missing_reference(app, item.xref, docname)
                        par.append(ref)
                        if i < len(items):
                            par.append(nodes.Text(", "))
            if excerpts and post.excerpt:
                for enode in post.excerpt:
                    enode = enode.deepcopy()
                    revise_pending_xrefs(enode, docname)
                    app.env.resolve_references(enode, docname, app.builder)
                    enode.parent = bli.parent
                    bli.append(enode)

        node.replace_self(bl)


def missing_reference(app, env, node, contnode):
    target = node["reftarget"]
    logging.debug(f"missing reference: {target}, {contnode}")
    return _missing_reference(app, target, node.get("refdoc"), contnode, node.get("refexplicit"))


def _missing_reference(app, target, refdoc, contnode=None, refexplicit=False):

    blog = Blog(app)
    if target in blog.references:
        docname, dispname = blog.references[target]

        if "html" in app.builder.name:
            internal = True
            uri = app.builder.get_relative_uri(refdoc, docname)
        else:
            internal = False
            uri = blog.blog_baseurl + "/" + docname

        newnode = nodes.reference("", "", internal=internal, refuri=uri, reftitle=dispname)
        if refexplicit:
            newnode.append(contnode)
        else:
            emp = nodes.emphasis()
            newnode.append(emp)
            emp.append(nodes.Text(text_type(dispname)))

        return newnode


def generate_archive_pages(app):
    """
    Generate archive pages for all posts, categories, tags, authors, and
    drafts.
    """

    if not ablog.builder_support(app):
        return

    blog = Blog(app)
    for post in blog.posts:
        for redirect in post.redirect:
            yield (redirect, {"redirect": post.docname, "post": post}, "redirect.html")

    found_docs = app.env.found_docs
    atom_feed = bool(blog.blog_baseurl)
    feed_archives = blog.blog_feed_archives
    blog_path = blog.blog_path
    for title, header, catalog in [
        (_("Authors"), _("Posts by"), blog.author),
        (_("Locations"), _("Posts from"), blog.location),
        (_("Languages"), _("Posts in"), blog.language),
        (_("Categories"), _("Posts in"), blog.category),
        (_("All posts"), _("Posted in"), blog.archive),
        (_("Tags"), _("Posts tagged"), blog.tags),
    ]:

        if not catalog:
            continue

        context = {"parents": [], "title": title, "header": header, "catalog": catalog, "summary": True}
        if catalog.docname not in found_docs:
            yield (catalog.docname, context, "catalog.html")

        for collection in catalog:

            if not collection:
                continue
            context = {
                "parents": [],
                "title": f"{header} {collection}",
                "header": header,
                "collection": collection,
                "summary": True,
                "feed_path": collection.path if feed_archives else blog_path,
                "archive_feed": atom_feed and feed_archives,
            }
            context["feed_title"] = context["title"]
            if collection.docname not in found_docs:
                yield (collection.docname, context, "collection.html")

    # ppp = 5
    # for page, i in enumerate(range(0, len(blog.posts), ppp)):
    if 1:
        context = {
            "parents": [],
            "title": _("All Posts"),
            "header": _("All"),
            "collection": blog.posts,
            "summary": True,
            "atom_feed": atom_feed,
            "feed_path": blog.blog_path,
        }
        docname = blog.posts.docname
        # if page:
        #    docname += '/' + str(page)
        yield (docname, context, "collection.html")

    context = {"parents": [], "title": _("Drafts"), "collection": blog.drafts, "summary": True}
    yield (blog.drafts.docname, context, "collection.html")


def generate_atom_feeds(app):
    """
    Generate archive pages for all posts, categories, tags, authors, and
    drafts.
    """

    if not ablog.builder_support(app):
        return

    blog = Blog(app)

    url = blog.blog_baseurl
    if not url:
        return

    feed_path = os.path.join(app.builder.outdir, blog.blog_path, "atom.xml")

    feeds = [
        (
            blog.posts,
            blog.blog_path,
            feed_path,
            blog.blog_title,
            os_path_join(url, blog.blog_path, "atom.xml"),
        )
    ]

    if blog.blog_feed_archives:

        for header, catalog in [
            (_("Posts by"), blog.author),
            (_("Posts from"), blog.location),
            (_("Posts in"), blog.language),
            (_("Posts in"), blog.category),
            (_("Posted in"), blog.archive),
            (_("Posts tagged"), blog.tags),
        ]:

            for coll in catalog:
                # skip collections containing only drafts
                if not len(coll):
                    continue
                folder = os.path.join(app.builder.outdir, coll.path)
                if not os.path.isdir(folder):
                    os.makedirs(folder)

                feeds.append(
                    (
                        coll,
                        coll.path,
                        os.path.join(folder, "atom.xml"),
                        blog.blog_title + " - " + header + " " + text_type(coll),
                        os_path_join(url, coll.path, "atom.xml"),
                    )
                )

    # Config options
    feed_length = blog.blog_feed_length
    feed_fulltext = blog.blog_feed_fulltext

    for feed_posts, pagename, feed_path, feed_title, feed_url in feeds:

        feed = FeedGenerator()
        feed.id("http://lernfunk.de/media/654321")
        feed.title(feed_title)
        feed.link(href=url)
        feed.subtitle(blog.blog_feed_subtitle)
        feed.link(href=feed_url)
        feed.language("en")
        feed.generator("ABlog", ablog.__version__, "https://ablog.readthedocs.org")

        for i, post in enumerate(feed_posts):
            if feed_length and i == feed_length:
                break
            post_url = os_path_join(url, app.builder.get_target_uri(post.docname))
            if post.section:
                post_url += "#" + post.section

            if blog.blog_feed_titles:
                content = None
            else:
                content = post.to_html(pagename, fulltext=feed_fulltext)

            feed_entry = feed.add_entry()
            feed_entry.id(post_url)
            feed_entry.title(post.title)
            feed_entry.link(href=post_url)
            feed_entry.author({"name": author.name for author in post.author})
            feed_entry.pubDate(post.date.astimezone())
            feed_entry.updated(post.update.astimezone())
            feed_entry.content(content=content, type="html")

        parent_dir = os.path.dirname(feed_path)
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)

        with open(feed_path, "w", encoding="utf-8") as out:
            feed_str = feed.atom_str(pretty=True)
            out.write(feed_str.decode())

    if 0:
        # this is to make the function a generator
        # and make work for Sphinx 'html-collect-pages'
        yield


def register_posts(app):
    """
    Register posts found in the Sphinx build environment.
    """

    blog = Blog(app)
    for docname, posts in getattr(app.env, "ablog_posts", {}).items():
        for postinfo in posts:
            blog.register(docname, postinfo)
