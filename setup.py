from distutils.core import setup

__version__ = ''
with open('ablog/__init__.py') as inp:
  for line in inp:
      if (line.startswith('__version__')):
          exec(line.strip())
          break
#with open('README.rst') as inp:
#    long_description = inp.read()


setup(
    name='ablog',
    version=__version__,
    author='Ahmet Bakan',
    author_email='lordnapi@gmail.com',
    description='ABlog for blogging with Sphinx',
    #long_description=long_description,
    url='http://github.com/abakan/ablog',
    packages=['ablog'],
    package_dir={'ablog': 'ablog'},
    package_data={'ablog': ['templates/*.html']},
    license='MIT License',
    #keywords=('abstract syntax tree transformer, IPython magic'),
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
    requires=['Werkzeug', 'Sphinx'],
)
