import datetime
from pathlib import Path

from packaging.version import parse as _parse

import ablog

ablog_builder = "dirhtml"
ablog_website = "_website"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "sphinx.ext.extlinks",
    "sphinx_automodapi.automodapi",
    "sphinx_toolbox",
    "ablog",
    "alabaster",
    "nbsphinx",
    "myst_parser",
]

version = str(_parse(ablog.__version__))
project = "ABlog"
current_year = datetime.datetime.now().year
copyright = f"2014-{current_year}, ABlog Team"  # NOQA: A001
master_doc = "index"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
exclude_patterns = ["_build", "docs/manual/.ipynb_checkpoints"]
html_title = "ABlog"
html_use_index = True
html_domain_indices = False
html_show_sourcelink = True
html_favicon = "_static/ablog.ico"
blog_title = "ABlog"
blog_baseurl = "https://ablog.readthedocs.io/"
blog_locations = {
    "Pittsburgh": ("Pittsburgh, PA", "https://en.wikipedia.org/wiki/Pittsburgh"),
    "San Fran": ("San Francisco, CA", "https://en.wikipedia.org/wiki/San_Francisco"),
    "Denizli": ("Denizli, Turkey", "https://en.wikipedia.org/wiki/Denizli"),
}
blog_languages = {
    "en": ("English", None),
    "nl": ("Nederlands", None),
    "zh_CN": ("Chinese", None),
}
blog_default_language = "en"
language = "en"
blog_authors = {
    "Ahmet": ("Ahmet Bakan", "https://ahmetbakan.com"),
    "Luc": ("Luc Saffre", "https://saffre-rumma.net/luc/"),
    "Mehmet": ("Mehmet Gerçeker", "https://github.com/mehmetg"),
}
blog_feed_archives = True
blog_feed_fulltext = True
blog_feed_templates = {
    "atom": {
        "content": "{{ title }}{% for tag in post.tags %}" " #{{ tag.name|trim()|replace(' ', '') }}" "{% endfor %}",
    },
    "social": {
        "content": "{{ title }}{% for tag in post.tags %}" " #{{ tag.name|trim()|replace(' ', '') }}" "{% endfor %}",
    },
}
disqus_shortname = "https-ablog-readthedocs-io"
disqus_pages = True
fontawesome_link_cdn = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"
html_theme = "alabaster"
html_sidebars = {
    "**": [
        "about.html",  # Comes from alabaster
        "searchfield.html",  # Comes from alabaster
        "ablog/postcard.html",
        "ablog/recentposts.html",
        "ablog/tagcloud.html",
        "ablog/categories.html",
        "ablog/archives.html",
        "ablog/authors.html",
        "ablog/languages.html",
        "ablog/locations.html",
    ]
}
html_theme_options = {
    "travis_button": False,
    "github_user": "sunpy",
    "github_repo": "ablog",
    "description": "ABlog for blogging with Sphinx",
    "logo": "ablog.png",
}
github_username = "sunpy"
github_repository = "ablog"
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
extlinks = {
    "wiki": ("https://en.wikipedia.org/wiki/%s", "%s"),
    "issue": ("https://github.com/sunpy/ablog/issues/%s", "issue %s"),
    "pull": ("https://github.com/sunpy/ablog/pull/%s", "pull request %s"),
}
rst_epilog = """
.. _Sphinx: http://sphinx-doc.org/
.. _Python: https://python.org
.. _Disqus: https://disqus.com/
.. _GitHub: https://github.com/sunpy/ablog
.. _PyPI: https://pypi.python.org/pypi/ablog
.. _Read The Docs: https://readthedocs.org/
.. _Alabaster: https://github.com/bitprophet/alabaster
"""
locale_dirs = [str(Path(ablog.__file__).parent / Path("locales"))]
nitpicky = True
nitpick_ignore = []
for line in open("nitpick-exceptions"):
    if line.strip() == "" or line.startswith("#"):
        continue
    dtype, target = line.split(None, 1)
    target = target.strip()
    nitpick_ignore.append((dtype, target))
