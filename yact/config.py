import os
import sys
import yaml
import logging
from threading import Lock
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class InvalidConfigFile(Exception):
    """Raised when config cannot be parsed/opened"""
    pass


class MissingConfig(Exception):
    """Indicates the config file does not exist"""
    pass


class ConfigEditFailed(Exception):
    """
    Raised when a config edit/update is impossible
    due to mismatched data types
    """
    pass


def from_file(filename, directory=None, unsafe=False):
    """
    Convenience function to search for a config file and
    return a `Config` object. Searches some default
    locations (currently only cares about Linux systems)
    for the specified file. If a directory is passed in
    it will be checked first.
    """
    prefixes = ['/etc', '~/.config', os.path.abspath(os.path.curdir), os.path.abspath(os.path.pardir)]
    if directory:
        prefixes.insert(0, directory)
    if os.path.isfile(filename):
        logger.debug('Retrieving config from full path {}'.format(filename))
        path = filename
    else:
        logger.debug('Searching for path to {}'.format(filename))
        for p in prefixes:
            temp = os.path.join(p, filename)
            if os.path.exists(temp) and not os.path.isdir(temp):
                logger.debug("Found {} in {}".format(filename, p))
                path = temp
                break
        else:
            raise MissingConfig('{} does not exist'.format(filename))
    config = Config(filename=path, unsafe=unsafe)
    config.refresh()
    return config


class Config(object):
    """
    The `Config` object is a wrapper around YAML data.
    For most use cases, the basic functionality of
    reading a YAML file (extension does not matter) is
    sufficient.

    While not currently tested, unsafe loading of YAML
    files is supported using the unsafe flag.
    """
    def __init__(self, filename, unsafe=False):
        self.unsafe = unsafe
        self.filename = filename
        self._lock = Lock()
        self.ts_refreshed = None
        self.ts_refreshed_utc = None

    def refresh(self):
        with self._lock:
            try:
                with open(self.filename, 'r') as f:
                    if not self.unsafe:
                        self._data = yaml.safe_load(f)
                    else:
                        self._data = yaml.load(f)
                    self.ts_refreshed = datetime.now()
                    self.ts_refreshed_utc = datetime.utcnow()
            except Exception as e:  # TODO: Split out into handling file IO and parsing errors
                raise InvalidConfigFile('{} failed to load: {}'.format(self.filename, e))

    def get(self, key, default=None):
        """
        Retrieve the value of a key (or consecutive keys joined by periods)
        or default, similar to dict.get
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def set(self, key, value):
        """
        Set the value of a provided key (or nested keys joined by periods)
        to the provided value
        """
        self.__setitem__(key, value)


    def remove(self, key):
        """
        Remove an item from configuration file

        Establishes lock on configuration data, deletes config
        entry matching the passed in key. Saves updated configuration
        back to file.
        """
        with self._lock:
            namespace = key.split('.')
            data = self._data
            for name in namespace[:-1]:
                try:
                    data = data[name]
                except KeyError:
                    return  # Item already gone, no need to do anything
            try:
                data.pop(namespace[-1])
            except KeyError:
                return  # Same as above
        self.save()

    @property
    def sections(self):
        """
        Provided for users of the standard ConfigParser module.
        """
        with self._lock:
            return list(self._data.keys())

    def save(self):
        """
        Save current configuration back to file in YAML format

        Acquires configuration lock, opens file in overwrite mode ('w')
        and writes the output of yaml.dump to the file object.
        default_flow_style is set to false to force proper YAML formatting
        """
        with self._lock:
            with open(self.filename, 'w') as f:
                yaml.dump(self._data, f, default_flow_style=False)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.filename)

    def __getitem__(self, item):
        """
        Allow `Config` to behave as a dictionary.
        Supports nested lookups:

        ::

            >>> print(config['db'])
            {'db': {'host': 'localhost', 'port': 21707}}
            >>> print(config['db.host'])
            'localhost'
        """
        with self._lock:
            namespace = item.split('.')
            data = self._data
            for name in namespace:
                data = data[name]  # Allow keyerrors to bubble up
            return data

    def __setitem__(self, key, value):
        """
        Enable dict-like setting of config values.
        Supports nested updates:

        ::

            >>> print(config)
            {}
            >>> config['db.host'] = 'localhost'
            >>> print(config['db'])
            {'db': {'host': 'localhost'}}
            >>> config['db.port'] = 21707
            {'db': {'host': 'localhost', 'port': 21707}}
        """
        with self._lock:
            namespace = key.split('.')
            data = self._data
            for name in namespace[:-1]:
                if hasattr(data, 'get') and hasattr(data.get(name, {}), 'get'):
                    if data.get(name) is None:
                        data[name] = {}
                else:
                    raise ConfigEditFailed("Unable to set {}: {} is an invalid child of {}".format(key, name, data))
                data = data[name]
            data[namespace[-1]] = value
        self.save()
