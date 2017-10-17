import os
import shutil
import hashlib
import unittest
from time import sleep

import yact


class test_yact(unittest.TestCase):

    @property
    def sample_cfg(self):
        shutil.copyfile(os.path.join(os.path.curdir, 'sample.yaml'),
         os.path.join(os.path.curdir, 'sample.testing'))  # Overwrites existing test file with sample.conf
        return os.path.join(os.path.curdir, 'sample.testing')

    def test_from_file(self):
        """
        Check instantiation from path, filename
        """
        test_files = ['test.yaml', os.path.join(os.path.curdir, 'test.yaml')]
        for tf in test_files:
            config = yact.from_file(tf, 'tests')
            self.assertIsInstance(config, yact.Config)
        with self.assertRaises(yact.MissingConfig):
            _ = yact.from_file('bogusfile')

    def test_remove(self):
        config = yact.from_file(self.sample_cfg)
        config.set('temporary', True)
        self.assertEqual(config['temporary'], True)
        config.remove('temporary')
        with self.assertRaises(KeyError):
            config['temporary']
        config.remove('temporary') # Shouldn't error out
        config.set('foo.bar.baz', True)
        config.set('foo.bar.bat', True)
        config.remove('foo.bar')
        config.remove('foo.bar.baz')
        config['foo']
        config.remove('foo')

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

    def test_md5sum(self):
        # First, let's test the fresh config file
        with open(self.sample_cfg, 'r') as f:
            md5 = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        config = yact.from_file(self.sample_cfg)
        # If all is good, the raw md5sum and the one provided by yact will match
        self.assertEqual(config.md5sum, md5)

        # This is a bit tricky, we copy a file every time self.sample_cfg
        # is accessed so we need to know the current filename config uses
        config.set('thischanged', True)
        with open(config.filename, 'r') as f:
            newmd5 = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        self.assertEqual(newmd5, config.md5sum)
        self.assertNotEqual(newmd5, md5)

    def test_config_file_changed(self):
        config = yact.from_file(self.sample_cfg)
        with open(config.filename, 'a') as f:
            f.write('modified: True')
        self.assertTrue(config.config_file_changed)

    def test_autoreload(self):
        config = yact.from_file(self.sample_cfg, auto_reload=True)
        oldmd5 = config.md5sum
        with open(config.filename, 'a') as f:
            f.write('modified: True')
        sleep(6)
        # By now yact should have refreshed, let's verify
        self.assertNotEqual(oldmd5, config.md5sum)


if __name__ == "__main__":
    unittest.main()
