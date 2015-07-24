# -*- coding: utf-8 -*-
"""post and postlist directives."""

import os
import sys
from string import Formatter
from datetime import datetime
try:
    from dateutil.parser import parse as date_parser
except ImportError:
    date_parser = None

from docutils import nodes
from sphinx.locale import _
from sphinx.util.nodes import set_source_info
from sphinx.util.compat import Directive, make_admonition
from docutils.parsers.rst import directives
from docutils.utils import relative_path

import ablog
from .blog import Blog, slugify, os_path_join, revise_pending_xrefs

if sys.version_info >= (3, 0):
    text_type = str
else:
    text_type = unicode


class PostNode(nodes.Element):
    """Represent ``post`` directive content and options in document tree."""

    pass


class PostList(nodes.General, nodes.Element):
    """Represent ``postlist`` directive converted to a list of links."""

    pass


class UpdateNode(nodes.Admonition, nodes.Element):
    """Represent ``update`` directive."""

    pass


class PostDirective(Directive):
    """Handle ``post`` directives."""

    _split = lambda a: [s.strip() for s in (a or '').split(',') if s.strip()]

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'tags': _split,
        'author': _split,
        'category': _split,
        'location': _split,
        'language': _split,
        'redirect': _split,
        'title': lambda a: a.strip(),
        'image': int,
        'excerpt': int,
        'exclude': directives.flag,
    }

    def run(self):

        node = PostNode()
        node.document = self.state.document
        set_source_info(self, node)
        self.state.nested_parse(self.content, self.content_offset,
                                node, match_titles=1)

        node['date'] = self.arguments[0] if self.arguments else None
        node['tags'] = self.options.get('tags', [])
        node['author'] = self.options.get('author', [])
        node['category'] = self.options.get('category', [])
        node['location'] = self.options.get('location', [])
        node['language'] = self.options.get('language', [])
        node['redirect'] = self.options.get('redirect', [])
        node['title'] = self.options.get('title', None)
        node['image'] = self.options.get('image', None)
        node['excerpt'] = self.options.get('excerpt', None)
        node['exclude'] = 'exclude' in self.options
        return [node]


class UpdateDirective(Directive):

    has_content = True
    required_arguments = 1
    optional_arguments = 0#1
    final_argument_whitespace = True
    option_spec = {}

    def run(self):

        ad = make_admonition(UpdateNode, self.name, [_('Updated on')],
                             self.options,
                             self.content, self.lineno, self.content_offset,
                             self.block_text, self.state, self.state_machine)
        ad[0]['date'] = self.arguments[0] if self.arguments else ''
        set_source_info(self, ad[0])
        return ad


class PostListDirective(Directive):
    """Handle ``postlist`` directives."""

    _split = lambda a: set(s.strip() for s in a.split(','))
    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'tags': _split,
        'author': _split,
        'category': _split,
        'location': _split,
        'language': _split,
        'format': lambda a: a.strip(),
        'date': lambda a: a.strip(),
        'sort': directives.flag,
        'excerpts': directives.flag,
        'list-style': lambda a: a.strip(),
    }

    def run(self):

        node = PostList()
        node.document = self.state.document
        set_source_info(self, node)
        self.state.nested_parse(self.content, self.content_offset,
                                node, match_titles=1)

        node['length'] = int(self.arguments[0]) if self.arguments else None
        node['tags'] = self.options.get('tags', [])
        node['author'] = self.options.get('author', [])
        node['category'] = self.options.get('category', [])
        node['location'] = self.options.get('location', [])
        node['language'] = self.options.get('language', [])
        node['format'] = self.options.get('format', '{date} - {title}')
        node['date'] = self.options.get('date', None)
        node['sort'] = 'sort' in self.options
        node['excerpts'] = 'excerpts' in self.options
        node['image'] = 'image' in self.options
        node['list-style'] = self.options.get('list-style', 'none')
        return [node]


def purge_posts(app, env, docname):
    """Remove post and reference to it from the standard domain when its
    document is removed or changed."""

    if hasattr(env, 'ablog_posts'):
        env.ablog_posts.pop(docname, None)

    filename = os.path.split(docname)[1]
    env.domains['std'].data['labels'].pop(filename, None)


def _get_section_title(section):
    """Return section title as text."""

    for title in section.traverse(nodes.title):
        break
    # A problem with the following is that title may contain pending
    # references, e.g. :ref:`tag-tips`
    return title.astext()


def _get_update_dates(section, docname, post_date_format):
    """Return list of dates of updates found section."""


    update_nodes = list(section.traverse(UpdateNode))
    update_dates = []
    for update_node in update_nodes:
        try:
            update = datetime.strptime(update_node['date'], post_date_format)
        except ValueError:
            raise ValueError('invalid post update date in: ' + docname)

        substitute = nodes.title(u'',
            update_node[0][0].astext() + u' ' + update.strftime(post_date_format))
        update_node[0].replace_self(substitute)
        # for now, let updates look like note
        update_node['classes'] = ['note', 'update']

        update_dates.append(update)
    return update_dates


def process_posts(app, doctree):
    """Process posts and map posted document names to post details in the
    environment."""

    env = app.builder.env
    if not hasattr(env, 'ablog_posts'):
        env.ablog_posts = {}

    post_nodes = list(doctree.traverse(PostNode))
    if not post_nodes:
        return
    post_date_format = app.config['post_date_format']
    docname = env.docname

    # mark the post as 'orphan' so that
    #   "document isn't included in any toctree" warning is not issued
    app.env.metadata[docname]['orphan'] = True

    blog = Blog(app)
    auto_excerpt = blog.post_auto_excerpt
    multi_post = len(post_nodes) > 1 or blog.post_always_section

    for order, node in enumerate(post_nodes, start=1):
        if node['excerpt'] is None:
            node['excerpt'] = auto_excerpt

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
        title = node['title'] or _get_section_title(section)

        # creating a summary here, before references are resolved
        excerpt = []
        if node.children:
            if node['exclude']:
                node.replace_self([])
            else:
                node.replace_self(node.children)
            for child in node.children:
                excerpt.append(child.deepcopy())
        elif node['excerpt']:
            count = 0
            for nod in section.traverse(nodes.paragraph):
                excerpt.append(nod.deepcopy())
                count += 1
                if count >= (node['excerpt'] or 0):
                    break
            node.replace_self([])
        else:
            node.replace_self([])
        nimg = node['image'] or blog.post_auto_image
        if nimg:
            for img, nod in enumerate(section.traverse(nodes.image), start=1):
                if img == nimg:
                    excerpt.append(nod.deepcopy())
                    break
        date = node['date']
        if date:
            try:
                date = datetime.strptime(date, post_date_format)
            except ValueError:
                if date_parser:
                    try:
                        date = date_parser(date)
                    except ValueError:
                        raise ValueError('invalid post date in: ' + docname)
                else:
                    raise ValueError('invalid post date in: ' + docname)

        else:
            date = None


        # if docname ends with `index` use folder name to reference the document
        # a potential problem here is that there may be files/folders with the
        #   same name, so issuing a warning when that's the case may be a good idea
        folder, label = os.path.split(docname)
        if label == 'index':
            folder, label = os.path.split(folder)
        if not label:
            label = slugify(title)

        section_name = ''
        if multi_post and section.parent is not doctree:
                section_name = section.attributes['ids'][0]
                label += '-' + section_name
        else:
            # create a reference for the post
            # if it is posting the document
            # ! this does not work for sections
            app.env.domains['std'].data['labels'][label] = (docname, label, title)

        if section.parent is doctree:
            section_copy = section[0].deepcopy()
        else:
            section_copy = section.deepcopy()

        # multiple posting may result having post nodes
        for nn in section_copy.traverse(PostNode):
            if nn['exclude']:
                nn.replace_self([])
            else:
                nn.replace_self(node.children)


        postinfo = {
            'docname': docname,
            'section': section_name,
            'order': order,
            'date': date,
            'update': max(update_dates + [date]),
            'title': title,
            'excerpt': excerpt,
            'tags': node['tags'],
            'author': node['author'],
            'category': node['category'],
            'location': node['location'],
            'language': node['language'],
            'redirect': node['redirect'],
            'image': node['image'],
            'exclude': node['exclude'],
            'doctree': section_copy
        }

        if docname not in env.ablog_posts:
            env.ablog_posts[docname] = []
        env.ablog_posts[docname].append(postinfo)


        non_html = 'html' not in app.builder.name

        # instantiate catalogs and collections here
        #  so that references are created and no warnings are issued
        if non_html:
            stdlabel = env.intersphinx_inventory.setdefault('std:label', {})
            baseurl = getattr(env.config, 'blog_baseurl').rstrip('/') + '/'
            project, version = env.config.project, text_type(env.config.version)
        else:
            stdlabel = env.domains['std'].data['labels']

        for key in ['tags', 'author', 'category', 'location', 'language']:
            catalog = blog.catalogs[key]
            for label in postinfo[key]:
                coll = catalog[label]

        if postinfo['date']:
            coll = blog.archive[postinfo['date'].year]


def process_postlist(app, doctree, docname):
    """Replace `PostList` nodes with lists of posts. Also, register all posts
    if they have not been registered yet."""

    blog = Blog()
    if not blog:
        register_posts(app)

    for node in doctree.traverse(PostList):
        colls = []
        for cat in ['tags', 'author', 'category', 'location', 'language']:
            for coll in node[cat]:
                if coll in blog.catalogs[cat].collections:
                    colls.append(blog.catalogs[cat].collections[coll])

        if colls:
            posts = set(blog.posts)
            for coll in colls:
                posts = posts & set(coll)
            posts = list(posts)
            posts.sort(reverse=True)
            posts = posts[:node.attributes['length']]
        else:
            posts = list(blog.recent(node.attributes['length'], docname,
                                          **node.attributes))

        if node.attributes['sort']:
            posts.sort() # in reverse chronological order, so no reverse=True

        fmts = list(Formatter().parse(node.attributes['format']))
        for text, key, __, __ in fmts:
            if key not in {'date', 'title', 'author', 'location', 'language',
                'category', 'tags'}:
                raise KeyError('{} is not recognized in postlist format'
                    .format(key))

        excerpts = node.attributes['excerpts']
        date_format = node.attributes['date'] or _(blog.post_date_format_short)
        bl = nodes.bullet_list()
        bl.attributes['classes'].append('post-list-style-' + node['list-style'])
        for post in posts:
            bli = nodes.list_item()
            bl.append(bli)
            par = nodes.paragraph()
            bli.append(par)


            for text, key, __, __ in fmts:
                if text:
                    par.append(nodes.Text(text))
                if key == 'date':
                    par.append(nodes.Text(post.date.strftime(date_format)))
                else:
                    if key == 'title':
                        items = [post]
                    else:
                        items = getattr(post, key)

                    for i, item in enumerate(items, start=1):
                        if key == 'title':
                            ref = nodes.reference()
                            ref['refuri'] = app.builder.get_relative_uri(docname, item.docname)
                            ref['ids'] = []
                            ref['backrefs'] = []
                            ref['dupnames'] = []
                            ref['classes'] = []
                            ref['names'] = []
                            ref['internal'] = True
                            emp = nodes.emphasis()
                            ref.append(emp)
                            emp.append(nodes.Text(text_type(item)))
                        else:
                            ref = _missing_reference(app, item.xref, docname)
                        par.append(ref)
                        if i < len(items):
                            par.append(nodes.Text(', '))
            if excerpts and post.excerpt:
                for enode in post.excerpt:
                    enode = enode.deepcopy()
                    revise_pending_xrefs(enode, docname)
                    app.env.resolve_references(enode, docname, app.builder)
                    enode.parent = bli.parent
                    bli.append(enode)

        node.replace_self(bl)


def missing_reference(app, env, node, contnode):

    target = node['reftarget']
    return _missing_reference(app, target, node['refdoc'],
                              contnode, node['refexplicit'])

def _missing_reference(app, target, refdoc, contnode=None, refexplicit=False):

    blog = Blog(app)
    if target in blog.references:
        docname, dispname = blog.references[target]

        if 'html' in app.builder.name:
            internal = True
            uri = app.builder.get_relative_uri(refdoc, docname)
        else:
            internal = False
            uri = blog.blog_baseurl + '/' + docname


        newnode = nodes.reference('', '', internal=internal, refuri=uri,
                                  reftitle=dispname)
        if refexplicit:
            newnode.append(contnode)
        else:
            emp = nodes.emphasis()
            newnode.append(emp)
            emp.append(nodes.Text(text_type(dispname)))

        return newnode

def generate_archive_pages(app):
    """Generate archive pages for all posts, categories, tags, authors, and
    drafts."""

    blog = Blog(app)
    for post in blog.posts:
        for redirect in post.redirect:
            yield (redirect, {'redirect': post.docname, 'post': post},
                   'redirect.html')

    atom_feed = bool(blog.blog_baseurl)
    feed_archives = blog.blog_feed_archives
    blog_path = blog.blog_path
    for title, header, catalog  in [
        (_('Authors'), _('Posts by'), blog.author),
        (_('Locations'), _('Posts from'), blog.location),
        (_('Languages'), _('Posts in'), blog.language),
        (_('Categories'), _('Posts in'), blog.category),
        (_('All posts'), _('Posted in'), blog.archive),
        (_('Tags'), _('Posts tagged'), blog.tags),]:

        if not catalog:
            continue

        context = {
            'parents': [],
            'title': title,
            'header': header,
            'catalog': catalog,
            'summary': True,
            'atom_feed': atom_feed,
            'feed_path': blog_path,
        }
        yield (catalog.docname, context, 'catalog.html')

        for collection in catalog:

            if not collection:
                continue
            context = {
                'parents': [],
                'title': u'{} {}'.format(header, collection),
                'header': header,
                'collection': collection,
                'summary': True,
                'atom_feed': atom_feed,
                'feed_path': collection.path if feed_archives else blog_path,
                'archive_feed': atom_feed and feed_archives
            }
            yield (collection.docname, context, 'collection.html')


    #ppp = 5
    #for page, i in enumerate(range(0, len(blog.posts), ppp)):
    if 1:
        context = {
            'parents': [],
            'title': _('All Posts'),
            'header': _('All'),
            'collection': blog.posts,
            'summary': True,
            'atom_feed': atom_feed,
            'feed_path': blog.blog_path,
        }
        docname = blog.posts.docname
        #if page:
        #    docname += '/' + str(page)
        yield (docname, context, 'collection.html')


    context = {
        'parents': [],
        'title': _('Drafts'),
        'collection': blog.drafts,
        'summary': True,
    }
    yield (blog.drafts.docname, context, 'collection.html')


def generate_atom_feeds(app):
    """Generate archive pages for all posts, categories, tags, authors, and
    drafts."""

    blog = Blog(app)


    url = blog.blog_baseurl
    if not url:
        raise StopIteration

    from werkzeug.contrib.atom import AtomFeed
    feed_path = os.path.join(app.builder.outdir, blog.blog_path, 'atom.xml')

    feeds = [(blog.posts,
             feed_path,
             blog.blog_title,
             os_path_join(url, blog.blog_path, 'atom.xml'))]

    if blog.blog_feed_archives:

        for header, catalog in [
            (_('Posts by'), blog.author),
            (_('Posts from'), blog.location),
            (_('Posts in'), blog.language),
            (_('Posts in'), blog.category),
            (_('Posted in'), blog.archive),
            (_('Posts tagged'), blog.tags),]:

            for coll in catalog:
                # skip collections containing only drafts
                if not len(coll):
                    continue
                folder = os.path.join(app.builder.outdir, coll.path)
                if not os.path.isdir(folder):
                    os.makedirs(folder)

                feeds.append((coll,
                          os.path.join(folder, 'atom.xml'),
                          blog.blog_title + u' - ' + header + u' ' + text_type(coll),
                          os_path_join(url, coll.path, 'atom.xml')))

    # Config options
    feed_length = blog.blog_feed_length
    feed_fulltext = blog.blog_feed_fulltext

    for feed_posts, feed_path, feed_title, feed_url in feeds:

        feed = AtomFeed(feed_title,
                        title_type='text',
                        url=url,
                        feed_url=feed_url,
                        subtitle=blog.blog_feed_subtitle,
                        generator=('ABlog', 'http://ablog.readthedocs.org',
                                   ablog.__version__))
        for i, post in enumerate(feed_posts):
            if feed_length and i == feed_length:
                break
            post_url = os_path_join(
                url, app.builder.get_target_uri(post.docname))
            if post.section:
                post_url += '#' + post.section

            if blog.blog_feed_titles:
                content = None
            else:
                content = post.to_html(blog.blog_path, fulltext=feed_fulltext)

            feed.add(post.title,
                     content=content,
                     title_type='text',
                     content_type='html',
                     author=', '.join(a.name for a in post.author),
                     url=post_url,
                     id=post_url,
                     updated=post.update, published=post.date)

        with open(feed_path, 'w') as out:
            feed_str = feed.to_string()
            try:
                out.write(feed_str.encode('utf-8'))
            except TypeError:
                out.write(feed_str)

    if 0:
        # this is to make the function a generator
        # and make work for Sphinx 'html-collect-pages'
        yield


def register_posts(app):
    """Register posts found in the Sphinx build environment."""

    blog = Blog()
    for docname, posts in getattr(app.env, 'ablog_posts', {}).items():
        for postinfo in posts:
            blog.register(docname, postinfo)
