import os
import re

from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name='click-params',
    python_requires='>=3.6',
    url='https://github.com/click-contrib/click_params',
    version=get_version('click_params'),
    author='Kevin Tewouda',
    author_email='lewoudar@gmail.com',
    description='A bunch of useful click parameter types',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    keywords='click params validators network',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click >= 7.0',
        'validators'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Terminals',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
