Quickstart
==========


.. _installation:

Installation
------------

Via Pip
~~~~~~~

To install YACT, run this in your terminal:

    $ pip install yact


Via Git
~~~~~~~

YACT is under active development on `GitHub <https://github.com/jesseops/yact>`_.

To install YACT via git, run this in your terminal:

    $ git clone git@github.com/jesseops/yact.git


Loading Config
--------------

YACT is designed to make loading your configuration as easy as possible. To that
end, calling `yact.from_file` with the name of your config file will automatically
search common locations and pull up your config. You may optionally give it a path
to search in if it's not in a standard location.

Example
~~~~~~~

Standard loading

    >>> import yact
    >>> config = yact.from_file('my-config.yaml')
    >>> print(config.filename)
    '/etc/my-config.yaml'

Explicit directory

    >>> config = yact.from_file('my-config.yaml', directory='/opt/my-app')
    >>> print(config.filename)
    '/opt/my-app/my-config.yaml'


Saving Config
-------------
