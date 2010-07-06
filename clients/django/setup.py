from setuptools import setup, find_packages
import os

version = '0.2.1'

setup(name='django_arecibo',
      version=version,
      description="Connector from Django to Arecibo",
      long_description=open("README.txt").read() + "\n",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Clearwind Consulting',
      author_email='andy@clearwind.ca',
      url='http://clearwind.ca',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'arecibo'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
