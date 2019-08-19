from setuptools import setup

__version__ = ''
with open('ablog/__init__.py') as inp:
    for line in inp:
        if (line.startswith('__version__')):
            exec(line.strip())
            break
long_description = '''
ABlog for Sphinx
================

Please note that is an official continuation of
`Eric Holscher's Ablog Sphinx extension <https://github.com/abakan/ablog/>`_.

A Sphinx extension that converts any documentation or personal website project
into a full-fledged blog. See http://ablog.readthedocs.org for details.

.. image:: https://secure.travis-ci.org/sunpy/ablog.png?branch=devel
   :target: http://travis-ci.org/#!/sunpy/ablog

.. image:: https://readthedocs.org/projects/ablog/badge/?version=latest
   :target: http://ablog.readthedocs.org/
'''

setup(
    name='ablog',
    version=__version__,
    author='SunPy Developers',
    author_email='nabil.freij@gmail.com',
    description='ABlog allows you to blog with Sphinx',
    long_description=long_description,
    url='http://ablog.readthedocs.org/',
    packages=['ablog'],
    package_dir={'ablog': 'ablog'},
    package_data={'ablog': [
        'templates/*.html',
        'locale/sphinx.pot',
        'locale/*/LC_MESSAGES/sphinx.*o']},
    license='MIT License',
    keywords=('Sphinx, extension, blogging, atom feeds'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    provides=['ablog'],
    install_requires=['werkzeug', 'sphinx>=1.6', 'alabaster', 'invoke',
                      'python-dateutil', 'sphinx-automodapi'],
    extra_requires={'notebook': ['nbsphinx', 'ipython']},
    message_extractors={
        'ablog': [
            ('**.html', 'jinja2', None),
            ('**.py', 'python', None),
        ]
    },
    entry_points={
        'console_scripts': [
            'ablog = ablog.commands:ablog_main',
        ],
    },
)
