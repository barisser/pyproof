from setuptools import setup

setup(
      name='pyproof',
      version='0.0.1',
      description='Solid as a Rock',
      license='MIT',
      install_requires=[
          'pycrypto'
        ],
      packages=['pyproof'],
      tests_require=[
          'pytest',
          'pytest-cov'
        ]
      )