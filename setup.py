from setuptools import setup, find_packages

setup(name='riqsolutions',
      version='0.1',
      description='Tools & packages to operationalize RiskIQ datasets',
      author='RiskIQ',
      author_email='support@riskiq.net',
      license='MIT',
      packages=find_packages(exclude=['tests*']),
      install_requires=[
          'requests',
      ],
      zip_safe=False)