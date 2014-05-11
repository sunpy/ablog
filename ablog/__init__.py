# -*- coding: utf-8 -*-
"""ABlog for Sphinx"""

import os
from datetime import datetime

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.nodes import set_source_info
from sphinx.util.compat import Directive
from sphinx.environment import dummy_reporter

from .ablog import ABlog, CONFIG

__version__ = '0.1'


class PostNode(nodes.Element):
    """Represent ``post`` directive content and options in document tree."""

    pass


class PostList(nodes.General, nodes.Element):
    """Represent ``postlist`` directive converted to a list of links."""

    pass


class PostDirective(Directive):
    """Handle ``post`` directives."""

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'tags': lambda a: [s.strip() for s in a.split(',')],
        'author': lambda a: [s.strip() for s in a.split(',')],
        'category': lambda a: [s.strip() for s in a.split(',')],
        'location': lambda a: [s.strip() for s in a.split(',')],
        'redirect': lambda a: [s.strip() for s in a.split(',')],
        'title': lambda a: a.strip(),
        'update': lambda a: a.strip(),
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
        node['update'] = self.options.get('update', None)
        node['tags'] = self.options.get('tags', [])
        node['author'] = self.options.get('author', [])
        node['category'] = self.options.get('category', [])
        node['location'] = self.options.get('location', [])
        node['redirect'] = self.options.get('redirect', [])
        node['title'] = self.options.get('title', None)
        node['image'] = self.options.get('image', None)
        node['excerpt'] = self.options.get('excerpt', None)
        node['exclude'] = 'exclude' in self.options
        return [node]


class PostListDirective(Directive):
    """Handle ``postlist`` directives."""

    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'tags': lambda a: set(s.strip() for s in a.split(',')),
        'author': lambda a: set(s.strip() for s in a.split(',')),
        'category': lambda a: set(s.strip() for s in a.split(',')),
        'location': lambda a: set(s.strip() for s in a.split(',')),
        'reverse': directives.flag,
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
        node['reverse'] = 'reverse' in self.options
        return [node]


def purge_posts(app, env, docname):
    """Remove post and reference to it in the standard domain when its
    document is removed or changed."""

    if hasattr(env, 'ablog_posts'):
        env.ablog_posts.pop(docname, None)
    env.domains['std'].data['labels'].pop(os.path.split(docname)[1], None)


def process_posts(app, doctree):
    """Process posts and map posted document names to post details in the
    environment."""

    env = app.builder.env
    if not hasattr(env, 'ablog_posts'):
        env.ablog_posts = {}
    post_nodes = list(doctree.traverse(PostNode))
    if not post_nodes:
        return
    docname = env.docname
    node = post_nodes[0]
    if len(post_nodes) > 1:
        env.warn(docname, 'multiple post directives found, '
                 'first one is considered')

    # Making sure that post has a title because all post titles
    # are needed when resolving post lists in documents
    title = node['title']
    if not title:
        for title in doctree.traverse(nodes.title):
            break
        # A problem with the following is that title may contain pending
        # references, e.g. :ref:`tag-tips`
        title = title.astext()

    # creating a summary here, before references are resolved
    excerpt = []
    if node.children:
        if node['exclude']:
            node.replace_self([])
        else:
            node.replace_self(node.children)
        for child in node.children:
            excerpt.append(child.deepcopy())
    else:
        count = 0
        for nod in doctree.traverse(nodes.paragraph):
            excerpt.append(nod.deepcopy())
            count += 1
            if count >= (node['excerpt'] or 0):
                break
        node.replace_self([])
    if node['image']:
        count = 0
        for nod in doctree.traverse(nodes.image):
            count += 1
            if count == node['image']:
                excerpt.append(nod.deepcopy())
                break

    date = node['date']
    if date:
        try:
            date = datetime.strptime(date, app.config['post_date_format'])
        except ValueError:
            raise ValueError('invalid post published date in: ' + docname)
    else:
        date = None

    update = node['update']
    if update:
        try:
            update = datetime.strptime(update, app.config['post_date_format'])
        except ValueError:
            raise ValueError('invalid post update date in: ' + docname)
    else:
        update = date

    env.ablog_posts[docname] = postinfo = {
        'date': date,
        'update': update,
        'title': title,
        'excerpt': excerpt,
        'tags': node['tags'],
        'author': node['author'],
        'category': node['category'],
        'location': node['location'],
        'redirect': node['redirect'],
        'image': node['image'],
        'exclude': node['exclude']}

    # if docname ends with `index` use folder name to reference the document
    # a potential problem here is that there may be files/folders with the
    #   same name, so issuing a warning when that's the case may be a good idea
    folder, label = os.path.split(docname)
    if label == 'index':
        folder, label = os.path.split(folder)
    app.env.domains['std'].data['labels'][label] = (docname, label, title)

    # mark the post as 'orphan' so that
    #   "document isn't included in any toctree" warning is not issued
    app.env.metadata[docname]['orphan'] = True

    # instantiate catalogs and collections here
    #  so that references are created and no warnings are issued

    ablog = ABlog(app)
    for key in ['tags', 'author', 'category', 'location']:
        catalog = ablog.catalogs[key]
        for label in postinfo[key]:
            catalog[label]
    if postinfo['date']:
        ablog.archive[postinfo['date'].year]


def process_postlist(app, doctree, docname):
    """Replace `PostList` nodes with lists of posts. Also, register all posts
    if they have not been registered yet."""

    ablog = ABlog()
    if not ablog:
        register_posts(app)

    for node in doctree.traverse(PostList):
        posts = list(ablog.recent(node.attributes['length'], docname,
                                      **node.attributes))
        if node.attributes['reverse']:
            posts.sort() # in reverse chronological order, so no reverse=True
        bl = nodes.bullet_list()
        for post in posts:
            bli = nodes.list_item()
            bl.append(bli)
            par = nodes.paragraph()

            if True:
                par.append(nodes.Text(
                    post.date.strftime(ablog.post_date_format) + ' - '))

            bli.append(par)
            ref = nodes.reference()
            ref['refuri'] = post.docname
            ref['ids'] = []
            ref['backrefs'] = []
            ref['dupnames'] = []
            ref['classes'] = []
            ref['names'] = []
            ref['internal'] = True
            par.append(ref)

            emp = nodes.emphasis()
            ref.append(emp)
            emp.append(nodes.Text(post.title))

        node.replace_self(bl)


def generate_archive_pages(app):
    """Generate archive pages for all posts, categories, tags, authors, and
    drafts."""

    ablog = ABlog(app)
    for post in ablog.posts:
        for redirect in post.redirect:
            yield (redirect, {'redirect': post.docname, 'post': post},
                   'redirect.html')

    for title, header, catalog in [
        (None, 'Posts by', ablog.author),
        (None, 'Posts from', ablog.location),
        (None, 'Posts in', ablog.category),
        ('All posts', 'Posted in', ablog.archive),
        (None, 'Posts tagged', ablog.tags),]:

        if not len(catalog):
            continue

        context = {
            'parents': [],
            'title': title or '{} {}'.format(header, catalog),
            'header': header,
            'catalog': catalog,
            'summary': True,
        }
        yield (catalog.docname, context, 'archive.html')

        for collection in catalog:

            if not len(collection):
                continue

            context = {
                'parents': [],
                'title': '{} {}'.format(header, collection),
                'header': header,
                'catalog': [collection],
                'summary': True,
            }
            yield (collection.docname, context, 'archive.html')

    context = {
        'parents': [],
        'title': 'Drafts',
        'archive': [ablog.drafts],
        'summary': True,
    }
    yield (collection.docname, context, 'archive.html')

    d = ablog.std_domain.data#['labels']
    #l = d.keys()
    #l.sort()
    #for k in l:
    #    print k, d[k]if
    url = ablog.blog_baseurl
    if not url:
        return

    from werkzeug.contrib.atom import AtomFeed
    feed_path  = os.path.join(app.builder.outdir, ablog.blog_path, 'atom.xml')
    feed = AtomFeed(ablog.blog_title,
                    title_type='text',
                    url=url,
                    feed_url=os.path.join(url, feed_path),
                    subtitle=ablog.blog_feed_subtitle)
    from datetime import datetime
    for post in ablog.posts:
        feed.add(post.title,
                 content=post.summary(ablog.blog_path),
                 title_type='text',
                 content_type='html',
                 author=', '.join(a.name for a in post.author),
                 url=os.path.join(url, post.docname),
                 id='post.uid' + str(post),
                 updated=post.update, published=post.date)

    with open(feed_path, 'w') as out:
        out.write(feed.to_string())



def init_ablog(app):
    """Instantiate ABlog, link from Sphinx app and `html_context`, and
    register posts."""

    # include in html context so that it can be reached from templates
    app.config.html_context['ablog'] = ABlog(app)


def register_posts(app):

    ablog = ABlog()
    for docname, postinfo in getattr(app.env, 'ablog_posts', {}).items():
        ablog.register(docname, postinfo)

    return
    from sphinx.util.console import bold, purple, darkgreen, term_width_line
    ablog_posts = getattr(app.env, 'ablog_posts', {})
    iterator = ablog_posts.keys()
    for docname in app.builder.status_iterator(iterator,
        'registering posts... ', purple, 50):
        ablog.register(docname, ablog_posts[docname])


def setup(app):
    """Setup ABlog extension."""

    for args in CONFIG:
        app.add_config_value(*args)

    app.add_directive('post', PostDirective)
    app.add_directive('postlist', PostListDirective)
    app.connect('builder-inited', init_ablog)
    app.connect('doctree-read', process_posts)
    app.connect('env-purge-doc', purge_posts)
    app.connect('doctree-resolved', process_postlist)
    app.connect('html-collect-pages', generate_archive_pages)


def get_html_templates_path():
    """Return path to the folder containing ABlog templates."""

    return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'templates')
