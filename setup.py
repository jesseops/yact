from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

__version__ = "0.0.1"
__desc__ = """An easy to use config package"""


with open(path.join(here, 'requirements.txt')) as r:
    __requires__ = [x.strip() for x in r.readlines() if not x.startswith('--')]

with open(path.join(here, 'readme.rst')) as f:
    __longdesc__ = f.read()

setup(
    name="figgypudding",
    author="Jesse Roberts",
    author_email="jesse@hackedpotatoes.com",
    version=__version__,
    url="http://hackedpotatoes.com",
    install_requires=__requires__,
    extras_require={'test': ['nosetests']},
    packages=['figgypudding'],
    description=__desc__,
    long_description=__longdesc__,
    license='MIT',
    keywords='yaml config parser pudding configuration',
    classifiers=[
        'Development STatus :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Configuration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
