============
YACT - Yet Another Config tool
============
Simple configuration handling for Python applications.
------------------------------------------------------
.. image :: https://travis-ci.org/dreadpirate15/yact.svg?branch=master
    :target: https://travis-ci.org/dreadpirate15/yact

.. image :: https://coveralls.io/repos/github/dreadpirate15/yact/badge.svg?branch=master
    :target: https://coveralls.io/github/dreadpirate15/yact?branch=master

YACT is a simple, lightweight, and flexible configuration package for Python applications.
It's designed to be as easy as possible to setup configuration for your project without needing to
jump through hoops.

Examples
========

**Basic usage:**

::

    import yact
    config = yact.from_file('sample.conf')
    isinstance(config, yact.Config)
    >>> True

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
