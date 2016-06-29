from setuptools import setup, find_packages
import os

version = '1.2.0dev'

tests_require = [
    'ftw.builder',
    'ftw.testbrowser',
    'ftw.testing',
]

setup(name='ftw.glossary',
      version=version,
      description="Content Type for defining terms in a glossary",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Lukas Graf',
      author_email='code@lukas-graf.ch',
      url='http://www.4teamwork.ch',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.js.jqueryui',
          'Products.TextIndexNG3',
          'Plone',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=[],
      )
