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

**Basic usage:**

::

    from figgypudding import Pudding
    config = Pudding.from_file('sample.conf')

**Modifying and saving:**

::

    config.set('foo', 'bar')
    print(config['foo'])
    >>> 'bar'
    config.save()

**Dot notation for nested configs:**

::

    config.set('this.is.nested', True)
    print(config.get('this')['is']['nested'])
    >>> True
