import os
import sys
import yaml
import logging
from threading import Lock
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


def from_file(filename, directory=None):
    return Config.from_file(filename, directory=directory)


class MissingConfig(Exception):
    pass


class ConfigEditFailed(Exception):
    pass


class Config(object):
    def __init__(self, file, safe_load=True):
        self.safe_load = safe_load
        self.filename = file
        self._lock = Lock()
        self.refreshed = None
        self.refreshed_utc = None

    def refresh(self):
        with self._lock:
            with open(self.filename, 'r') as f:
                if self.safe_load:
                    self._data = yaml.safe_load(f)
                else:
                    self._data = yaml.load(f)
                self.refreshed = datetime.now()
                self.refreshed_utc = datetime.utcnow()

    def get(self, key, default=None):
        with self._lock:
            namespace = key.split('.')
            temp = self._data
            while namespace:
                temp = temp.get(namespace.pop(0))
                if not temp:
                    return default
            return temp

    def set(self, key, value):
        with self._lock:
            namespace = key.split('.')
            data = self._data
            for name in namespace[:-1]:
                if not data.get(name):
                    data[name] = {}
                elif hasattr(data.get(temp), '__getitem__'):
                    pass  # No need to set it here
                else:
                    raise ConfigEditFailed("Unable to set {}: {} is type {}".format(
                        key,
                        name,
                        type(data[temp])
                    ))
                data = data[name]
            data[namespace[-1]] = value

    def remove(self, item):
        with self._lock:
            self._data.pop(item)

    @property
    def sections(self):
        with self._lock:
            return list(self._data.keys())

    @classmethod
    def from_file(cls, filename, directory=None):
        """
        Return `Config` from a given file, allowing for full path,
        relative path from
        """
        prefixes = ['/etc', '~/.config', os.path.abspath(os.path.curdir), os.path.abspath(os.path.pardir)]
        if directory:
            prefixes.insert(0, directory)
        if os.path.exists(filename) and not os.path.isdir(filename):
            logger.debug('Retrieving config from full path {}'.format(filename))
            path = filename
        else:
            logger.debug('Searching for path to {}'.format(filename))
            for p in prefixes:
                temp = os.path.join(p, filename)
                print(temp)
                if os.path.exists(temp) and not os.path.isdir(temp):
                    logger.debug("Found {} in {}".format(filename, p))
                    path = temp
                    break
            else:
                raise MissingConfig('{} does not exist'.format(filename))
        config = cls(file=path)
        config.refresh()
        return config

    def save(self):
        with self._lock:
            with open(self.filename, 'w') as f:
                yaml.dump(self._data, f, default_flow_style=False)

    def __repr__(self):
        return "<{} - {}>".format(self.__class__.__name__, self.filename)

    def __setattr__(self, attr, value):
        if attr not in ['safe_load', 'filename', '_lock', '_data', 'refreshed', 'refreshed_utc']:
            raise ConfigEditFailed("Setting config directly on {} is not allowed".format(self))
        else:
            super(Config, self).__setattr__(attr, value)

    def __getitem__(self, item):
        return self._data[item]
