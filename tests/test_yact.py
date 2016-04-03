import os
import shutil
import unittest
from time import sleep

import yact


class test_yact(unittest.TestCase):

    @property
    def sample_cfg(self):
        shutil.copyfile(os.path.join(os.path.curdir, 'sample.conf'),
         os.path.join(os.path.curdir, 'sample.testing'))  # Overwrites existing test file with sample.conf
        return os.path.join(os.path.curdir, 'sample.testing')

    def test_from_file(self):
        """
        Check instantiation from path, filename
        """
        test_files = ['test.conf', os.path.join(os.path.curdir, 'test.conf')]
        for tf in test_files:
            config = yact.from_file(tf, 'tests')
            self.assertIsInstance(config, yact.Config)
        with self.assertRaises(yact.MissingConfig):
            config = yact.from_file('bogusfile')

    def test_remove(self):
        config = yact.from_file(self.sample_cfg)
        config.set('temporary', True)
        self.assertEqual(config['temporary'], True)
        config.remove('temporary')
        with self.assertRaises(KeyError):
            config['temporary']
        config.remove('temporary') # Shouldn't error out

    def test_set(self):
        config = yact.from_file(self.sample_cfg)
        config.set('ham', 'spam')
        self.assertEqual(config['ham'], 'spam')
        config.set('spam.spam.spam', True)
        config.set('spam.with.ham.and.eggs', True)
        self.assertEqual(config['spam']['spam']['spam'], True)
        self.assertEqual(config['spam']['with']['ham']['and']['eggs'], True)
        config.set('menu', ['spam', 'spam', 'spam', 'spam'])
        with self.assertRaises(yact.ConfigEditFailed):
            config.set('menu.breakfast', False)  # Raise expection

    def test_setitem(self):
        config = yact.from_file(self.sample_cfg)
        config['ham'] = 'spam'
        self.assertEqual(config['ham'], 'spam')
        config['spam.ham'] = 'spam'
        self.assertEqual(config['spam']['ham'], 'spam')


    def test_get(self):
        config = yact.from_file(self.sample_cfg)  # Known entries
        self.assertEqual(config.get('environment'), 'development')
        self.assertEqual(config.get('db.missingentry'), None)

    def test_getitem(self):
        config = yact.from_file(self.sample_cfg) # Known entries
        self.assertEqual(config['environment'], 'development')
        self.assertEqual(config['db.host'], 'localhost')
        self.assertEqual(config['db']['host'], 'localhost')
        with self.assertRaises(KeyError):
            config['db.missingentry']
        with self.assertRaises(KeyError):
            config['missingentry']

    def test_save(self):
        config = yact.from_file(self.sample_cfg)

        new_filename = self.sample_cfg.replace('testing', 'yaml')
        config.filename = new_filename
        config.save()

        new_config = yact.from_file(new_filename)
        self.assertEqual(config._data, new_config._data)

    def test_refresh(self):
        config = yact.from_file(self.sample_cfg)
        loaded = config.ts_refreshed_utc
        sleep(2)
        config.refresh()
        refreshed = config.ts_refreshed_utc
        self.assertGreaterEqual((refreshed - loaded).total_seconds(), 2)

        config.filename = 'nonexistent'
        with self.assertRaises(yact.InvalidConfigFile):
            config.refresh()

    def test_unsafe_load(self):
        config = yact.from_file(self.sample_cfg, unsafe=True)

    def test_sections(self):
        config = yact.from_file(self.sample_cfg)
        self.assertIsInstance(config.sections, list)

    def test_repr(self):
        """
        Does repr do what I expect?
        """
        config = yact.from_file(self.sample_cfg)
        self.assertEqual(str(config), '{}({})'.format(config.__class__.__name__, self.sample_cfg))


if __name__ == "__main__":
    unittest.main()
