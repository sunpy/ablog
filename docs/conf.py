import re

import alabaster
from pkg_resources import get_distribution
from sphinx import addnodes

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
    "alabaster",
    "nbsphinx",
    "myst_parser",
    "ablog",
]

# PROJECT
versionmod = get_distribution("ablog")
myst_update_mathjax = False
# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# The short X.Y version.
version = ".".join(versionmod.version.split(".")[:3])
# The full version, including alpha/beta/rc tags.
release = versionmod.version.split("+")[0]
# Is this version a development release
is_development = ".dev" in release
project = "ABlog"
copyright = "2014-2021, ABlog Team"
master_doc = "index"
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
exclude_patterns = ["_build"]

# HTML OUTPUT
html_title = "ABlog"
html_static_path = ["_static"]
html_use_index = True
html_domain_indices = False
html_show_sourcelink = True
html_favicon = "_static/ablog.ico"

# ABLOG
blog_title = "ABlog"
blog_baseurl = "https://ablog.readthedocs.org"
blog_locations = {
    "Pittsburgh": ("Pittsburgh, PA", "https://en.wikipedia.org/wiki/Pittsburgh"),
    "SF": ("San Francisco, CA", "https://en.wikipedia.org/wiki/San_Francisco"),
    "Denizli": ("Denizli, Turkey", "https://en.wikipedia.org/wiki/Denizli"),
}
blog_languages = {"en": ("English", None)}
blog_default_language = "en"
blog_authors = {
    "Ahmet": ("Ahmet Bakan", "https://ahmetbakan.com"),
    "Luc": ("Luc Saffre", "https://saffre-rumma.net/luc/"),
    "Mehmet": ("Mehmet Gerçeker", "https://github.com/mehmetg"),
}
blog_feed_archives = True
blog_feed_fulltext = True
blog_feed_length = None
disqus_shortname = "ablogforsphinx"
disqus_pages = True
fontawesome_css_file = "css/font-awesome.css"

# THEME
html_style = "alabaster.css"
html_theme = "alabaster"
html_sidebars = {
    "**": [
        "about.html",
        "postcard.html",
        "recentposts.html",
        "tagcloud.html",
        "categories.html",
        "archives.html",
        "searchbox.html",
    ]
}
html_theme_path = [alabaster.get_path()]
html_theme_options = {
    "travis_button": False,
    "github_user": "sunpy",
    "github_repo": "ablog",
    "description": "ABlog for blogging with Sphinx",
    "logo": "ablog.png",
}

# SPHINX
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
extlinks = {
    "wiki": ("https://en.wikipedia.org/wiki/%s", ""),
    "issue": ("https://github.com/sunpy/ablog/issues/%s", "issue "),
    "pull": ("https://github.com/sunpy/ablog/pull/%s", "pull request "),
}
exclude_patterns = ["docs/manual/.ipynb_checkpoints/*"]
rst_epilog = """
.. _Sphinx: http://sphinx-doc.org/
.. _Python: https://python.org
.. _Disqus: https://disqus.com/
.. _GitHub: https://github.com/sunpy/ablog
.. _PyPI: https://pypi.python.org/pypi/ablog
.. _Read The Docs: https://readthedocs.org/
.. _Alabaster: https://github.com/bitprophet/alabaster
"""


def parse_event(env, sig, signode):
    event_sig_re = re.compile(r"([a-zA-Z-]+)\s*\((.*)\)")
    m = event_sig_re.match(sig)
    if not m:
        signode += addnodes.desc_name(sig, sig)
        return sig
    name, args = m.groups()
    signode += addnodes.desc_name(name, name)
    plist = addnodes.desc_parameterlist()
    for arg in args.split(","):
        arg = arg.strip()
        plist += addnodes.desc_parameter(arg, arg)
    signode += plist
    return name


def setup(app):
    from sphinx.ext.autodoc import cut_lines
    from sphinx.util.docfields import GroupedField

    app.connect("autodoc-process-docstring", cut_lines(4, what=["module"]))
    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
    )
    fdesc = GroupedField("parameter", label="Parameters", names=["param"], can_collapse=True)
    app.add_object_type("event", "event", "pair: %s; event", parse_event, doc_field_types=[fdesc])
