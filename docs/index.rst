.. YACT documentation master file, created by
   sphinx-quickstart on Wed Jun  1 11:20:08 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

YACT - A Pythonic approach to configuration
===========================================

Release v\ |version|. (:ref:`Installation <installation>`)

YACT is a friendly configuration tool that does all the heavy lifting so you don't have to.

Here's how easy it is::

    >>> config = yact.from_file('my-config.yaml')
    >>> config.get('debug')
    True

YACT allows you to write human readable configuration files using YAML, then
load that configuration into your app without having to set up parsers, or
search for config files, or any of that nonsense. Even better, YACT can
automatically reload your configuration file when it detects the file has
changed.::

    >>> config = yact.from_file('my-config.yaml', auto_reload=True)

YACT is tested against Python 2.7, 3.3-3.6 and PyPy.


Usage Guide
-----------

.. toctree::
   :maxdepth: 2

   usage/quickstart
   usage/advanced


API Documentation
-----------------

Here you will find documentation of the actual code. Wondering what exactly
`yact.from_file` does? This is for you.

.. toctree::
   ::maxdepth: 2

   api


Contribution Guide
------------------

.. toctree::
   :maxdepth: 2

   dev/contributing
   dev/todo
   dev/authors

