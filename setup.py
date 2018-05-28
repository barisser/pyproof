from setuptools import setup

setup(
    name='pyproof',
    author='Andrew Barisser',
    author_email='barisser@protonmail.com',
    version='0.0.1',
    url='https://github.com/barisser/pyproof',
    description='Solid as a Rock',
    license='MIT',
    install_requires=[
        'pycrypto'
        ],
    packages=['pyproof'],
    tests_require=[
        'numpy',
        'pytest',
        'pytest-cov',
        ]
      )
