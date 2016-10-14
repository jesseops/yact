from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

__version__ = "0.4.0"
__desc__ = """Yet Another Config Tool"""


with open(path.join(here, 'requirements.txt')) as r:
    __requires__ = [x.strip() for x in r.readlines() if not x.startswith('--')]

with open(path.join(here, 'readme.rst')) as f:
    __longdesc__ = f.read()

setup(
    name="yact",
    author="Jesse Roberts",
    author_email="jesse@hackedpotatoes.com",
    version=__version__,
    url="https://github.com/dreadpirate15/yact",
    install_requires=__requires__,
    extras_require={'test': ['nosetests']},
    packages=['yact'],
    description=__desc__,
    long_description=__longdesc__,
    license='MIT',
    keywords='yaml yact settings config parser pudding configuration',
    classifiers=[
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
