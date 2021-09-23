import os
import re
from setuptools import setup, find_packages

with open('riqsolutions/_version.py', 'r') as fd:
    v_match = re.search(r'^VERSION\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE)
    __version__ = v_match.group(1) if v_match else 'no version'

setup(name='riqsolutions',
      version=__version__,
      description='Tools & packages to operationalize RiskIQ datasets',
      author='RiskIQ',
      author_email='support@riskiq.net',
      license='MIT',
      packages=find_packages(exclude=['tests*']),
      install_requires=[
          'requests','lxml','xmltodict'
      ],
      zip_safe=False)
