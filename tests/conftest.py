import docutils
import pytest
import sphinx
from sphinx.testing.path import path

# Load app, status and warning fixtures.
pytest_plugins = ["sphinx.testing.fixtures"]


# inspired from sphinx's conftest.py
def pytest_report_header(config):
    header = "libraries: Sphinx-%s, docutils-%s" % (sphinx.__display_version__, docutils.__version__)
    if hasattr(config, "_tmp_path_factory"):
        header += "\nbase tempdir: %s" % config._tmp_path_factory.getbasetemp()

    return header


@pytest.fixture(scope="session")
def rootdir():
    return path(__file__).parent.abspath() / "roots"


@pytest.fixture(scope="function", autouse=True)
def reset_blog_config():
    # Reset cached configurations to enable confoverrides
    from ablog.blog import Blog

    Blog._dict = {}
