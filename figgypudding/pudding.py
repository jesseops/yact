import os
import yaml
import time
import logging
from threading import Lock
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class MissingConfig(Exception):
    pass


class Pudding(object):
    def __init__(self, file):
        self.filename = file
        self._lock = Lock()

    def refresh(self):
        with self._lock:
            with open(self.filename, 'r') as f:
                self._data = yaml.safe_load(f)
                self.refreshed = datetime.now()
                self.refreshed_utc = datetime.utcnow()

    def get(self, key):
        with self._lock:
            return self._data.get(key)

    def set(self, item, value):
        with self._lock:
            self._data[item] = value

    @property
    def sections(self):
        with self._lock:
            return list(self._data.keys())

    @classmethod
    def from_file(self, filename, directory=None):
        """
        Return Pudding from a given file, allowing for full path,
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
        pudding = Pudding(file=path)
        pudding.refresh()
        return pudding

    def save(self):
        with self._lock:
            with open(self.filename, 'w') as f:
                yaml.dump(self._data, f, default_flow_style=False)

    def __getitem__(self, item):
        return self._data[item]
