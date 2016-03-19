============
figgypudding
============
Simple configuration handling for Python applications.
------------------------------------------------------
.. image :: https://travis-ci.org/dreadpirate15/figgypudding.svg?branch=master
    :target: https://travis-ci.org/dreadpirate15/figgypudding

Figgypudding is a simple, lightweight, and flexible configuration package for Python applications.
It's designed to be as easy as possible to setup configuration for your project without needing to
jump through hoops.

Examples
========

::

    from figgypudding import Pudding
    config = Pudding.search('sample.conf')
