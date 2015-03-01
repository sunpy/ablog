import sys
from setuptools import setup

__version__ = ''
with open('ablog/__init__.py') as inp:
  for line in inp:
      if (line.startswith('__version__')):
          exec(line.strip())
          break
with open('README.rst') as inp:
    long_description = inp.read()

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
    package_data={'ablog': ['templates/*.html',
                            'locale/sphinx.pot',
                            'locale/*/LC_MESSAGES/sphinx.*o']},
    license='MIT License',
    keywords=('Sphinx, extension, blogging, atom feeds'),
    classifiers=[
                 'Development Status :: 3 - Alpha',
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
    install_requires=['Werkzeug', 'Sphinx'],
    message_extractors={
        'ablog': [
            ('**.html', 'jinja2', None),
            ('**.py',   'python', None),
        ]
    },
    entry_points = {
        'console_scripts': [
            'ablog = ablog.commands:ablog_main',
            'ablog%s = ablog.commands:ablog_main' % sys.version_info[0],
            ],
        'distutils.commands': [
            'ablog = ablog.commands:ablog_main',
            ],
        },
)
