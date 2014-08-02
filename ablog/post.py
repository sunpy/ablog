# -*- coding: utf-8 -*-
"""post and postlist directives."""

import os
from datetime import datetime

from docutils import nodes
from sphinx.locale import _
from sphinx.util.nodes import set_source_info
from sphinx.util.compat import Directive
from docutils.parsers.rst import directives

import ablog
from .blog import Blog, slugify

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
    if app.config.skip_pickling:
        env.topickle = lambda *args: env.warn('index',
            'Environment is not being pickled.')
    if not hasattr(env, 'ablog_posts'):
        env.ablog_posts = {}

    post_nodes = list(doctree.traverse(PostNode))
    if not post_nodes:
        return

    docname = env.docname

    # mark the post as 'orphan' so that
    #   "document isn't included in any toctree" warning is not issued
    app.env.metadata[docname]['orphan'] = True

    blog = Blog(app)
    multi_post = len(post_nodes) > 1 or blog.post_always_section
    for order, node in enumerate(post_nodes, start=1):

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

        # Making sure that post has a title because all post titles
        # are needed when resolving post lists in documents
        title = node['title']
        if not title:
            for title in section.traverse(nodes.title):
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
            for nod in section.traverse(nodes.paragraph):
                excerpt.append(nod.deepcopy())
                count += 1
                if count >= (node['excerpt'] or 0):
                    break
            node.replace_self([])
        if node['image']:
            count = 0
            for nod in section.traverse(nodes.image):
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

        # if docname ends with `index` use folder name to reference the document
        # a potential problem here is that there may be files/folders with the
        #   same name, so issuing a warning when that's the case may be a good idea
        folder, label = os.path.split(docname)
        if label == 'index':
            folder, label = os.path.split(folder)
        if not label:
            label = slugify(title)


        post_name = docname
        section_name = ''

        if multi_post and section.parent is not doctree:
                section_name = section.attributes['ids'][0]
                post_name = docname + '#' + section_name
                label += '-' + section_name

        # create a reference for the post
        app.env.domains['std'].data['labels'][label] = (docname, label, title)


        postinfo = {
            'docname': docname,
            'section': section_name,
            'order': order,
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

        if docname not in env.ablog_posts:
            env.ablog_posts[docname] = []
        env.ablog_posts[docname].append(postinfo)


        # instantiate catalogs and collections here
        #  so that references are created and no warnings are issued

        for key in ['tags', 'author', 'category', 'location']:
            catalog = blog.catalogs[key]
            for label in postinfo[key]:
                catalog[label]
        if postinfo['date']:
            blog.archive[postinfo['date'].year]


def process_postlist(app, doctree, docname):
    """Replace `PostList` nodes with lists of posts. Also, register all posts
    if they have not been registered yet."""

    blog = Blog()
    if not blog:
        register_posts(app)

    for node in doctree.traverse(PostList):
        posts = list(blog.recent(node.attributes['length'], docname,
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
                    post.date.strftime(blog.post_date_format) + ' - '))

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

    blog = Blog(app)
    for post in blog.posts:
        for redirect in post.redirect:
            yield (redirect, {'redirect': post.docname, 'post': post},
                   'redirect.html')
    for title, header, catalog in [
        (_('Authors'), _('Posts by'), blog.author),
        (_('Locations'), _('Posts from'), blog.location),
        (_('Categories'), _('Posts in'), blog.category),
        (_('All posts'), _('Posted in'), blog.archive),
        (_('Tags'), _('Posts tagged'), blog.tags),]:

        if not len(catalog):
            continue

        context = {
            'parents': [],
            'title': title,
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
                'title': u'{} {}'.format(header, collection),
                'header': header,
                'catalog': [collection],
                'summary': True,
            }
            yield (collection.docname, context, 'archive.html')

    context = {
        'parents': [],
        'title': _('Drafts'),
        'catalog': [blog.drafts],
        'summary': True,
    }
    yield (blog.drafts.docname, context, 'archive.html')

    url = blog.blog_baseurl
    if not url:
        return

    from werkzeug.contrib.atom import AtomFeed
    feed_path = os.path.join(app.builder.outdir, blog.blog_path, 'atom.xml')
    feed = AtomFeed(blog.blog_title,
                    title_type='text',
                    url=url,
                    feed_url=os.path.join(url, blog.blog_path, 'atom.xml'),
                    subtitle=blog.blog_feed_subtitle,
                    generator=('ABlog', 'http://blog.readthedocs.org',
                               ablog.__version__))
    for post in blog.posts:
        post_url = os.path.join(url, post.docname)
        feed.add(post.title,
                 content=post.summary(blog.blog_path),
                 title_type='text',
                 content_type='html',
                 author=', '.join(a.name for a in post.author),
                 url=post_url,
                 id=post_url,
                 updated=post.update, published=post.date)

    with open(feed_path, 'w') as out:
        out.write(feed.to_string().encode('utf-8'))


def register_posts(app):
    """Register posts found in the Sphinx build environment."""

    blog = Blog()
    for docname, posts in getattr(app.env, 'ablog_posts', {}).items():
        for postinfo in posts:
            blog.register(docname, postinfo)
