import sys
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

A Sphinx extension that converts any documentation or personal website project
into a full-fledged blog. See http://ablog.readthedocs.org for details.

.. image:: https://secure.travis-ci.org/abakan/ablog.png?branch=devel
   :target: http://travis-ci.org/#!/abakan/ablog

.. image:: https://readthedocs.org/projects/ablog/badge/?version=latest
   :target: http://ablog.readthedocs.org/
'''

setup(
    name='ablog',
    version=__version__,
    author='Ahmet Bakan',
    author_email='lordnapi@gmail.com',
    description='ABlog for blogging with Sphinx',
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
    provides=['ablog ({0:s})'.format(__version__)],
    install_requires=['Werkzeug', 'Sphinx', 'alabaster', 'invoke', 'python-dateutil'],
    message_extractors={
        'ablog': [
            ('**.html', 'jinja2', None),
            ('**.py',   'python', None),
        ]
    },
    entry_points = {
        'console_scripts': [
            'ablog = ablog.commands:ablog_main',
            'ablog{} = ablog.commands:ablog_main'.format(sys.version_info[0]),
            ],
        },
)
