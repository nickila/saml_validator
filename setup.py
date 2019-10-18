import os

from setuptools import setup, find_packages

from backend_app._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

test_deps = ['pytest']


def package_files(*dirs):
    paths = []
    for d in dirs:
        for (path, directories, filenames) in os.walk(d):
            for filename in filenames:
                paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('backend_app/resources')

setup(name='backend_app',
      version=__version__,
      description='SAML Analyzer',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[],
      url='https://github.com/michaelmernin/flask_saml_validator',
      maintainer='Michael Mernin, Brian Nickila, Danimae Vossen',
      maintainer_email='',
      license='MIT',
      package_data={
          'backend_app': extra_files,
      },
      packages=find_packages(),
      install_requires=[
          'xmltodict',
          'Flask',
          'PyYAML',
      ],
      tests_require=test_deps,
      )
