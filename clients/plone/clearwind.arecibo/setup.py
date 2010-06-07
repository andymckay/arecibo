from setuptools import setup, find_packages
import os

version = '0.3'

setup(name='clearwind.arecibo',
      version=version,
      description="Connector from Plone to Arecibo",
      long_description=open("README.txt").read() + "\n",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='ClearWind Consulting',
      author_email='andy@clearwind.ca',
      url='http://clearwind.ca',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['clearwind'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
