import os
import unittest
from time import sleep

import yact


class test_yact(unittest.TestCase):
    SAMPLE_CFG = os.path.join(os.path.curdir, 'sample.conf')

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
        config = yact.from_file(self.SAMPLE_CFG)
        config.set('temporary', True)
        self.assertEqual(config['temporary'], True)
        config.remove('temporary')
        with self.assertRaises(KeyError):
            config['temporary']
        config.remove('temporary') # Shouldn't error out

    def test_set(self):
        config = yact.from_file(self.SAMPLE_CFG)
        config.set('set', 'go')
        self.assertEqual(config['set'], 'go')
        config.set('this.must.nest', True)
        config.set('this.must.be.nested', True)
        self.assertEqual(config['this']['must']['nest'], True)
        self.assertEqual(config['this']['must']['be']['nested'], True)
        config.set('this.is.a.list', [1,2,3])
        with self.assertRaises(yact.ConfigEditFailed):
            config.set('this.is.a.list.not', False)  # Raise expection

    def test_get(self):
        config = yact.from_file(self.SAMPLE_CFG)
        self.assertEqual(config.get('ham.eggs.bar'), 1)
        self.assertEqual(config.get('haml.eggs.spam.this.does.not.exist'), None)

    def test_getitem(self):
        config = yact.from_file(self.SAMPLE_CFG)
        self.assertEqual(config['ham']['eggs']['bar'], 1)
        self.assertEqual(config['ham.eggs.bar'], 1)
        with self.assertRaises(KeyError):
            config['nonexistent']

    def test_save(self):
        config = yact.from_file(self.SAMPLE_CFG)

        new_filename = self.SAMPLE_CFG.replace('conf', 'yaml')
        config.filename = new_filename
        config.save()

        new_config = yact.from_file(new_filename)
        self.assertEqual(config._data, new_config._data)

    def test_refresh(self):
        config = yact.from_file(self.SAMPLE_CFG)
        loaded = config.ts_refreshed_utc
        sleep(2)
        config.refresh()
        refreshed = config.ts_refreshed_utc
        self.assertGreaterEqual((refreshed - loaded).total_seconds(), 2)

        config.filename = 'nonexistent'
        with self.assertRaises(yact.InvalidConfigFile):
            config.refresh()

    def test_unsafe_load(self):
        config = yact.from_file(self.SAMPLE_CFG, unsafe=True)

    def test_sections(self):
        config = yact.from_file(self.SAMPLE_CFG)
        self.assertIsInstance(config.sections, list)

    def test_repr(self):
        """
        Does repr do what I expect?
        """
        config = yact.from_file(self.SAMPLE_CFG)
        self.assertEqual(str(config), '{}({})'.format(config.__class__.__name__, self.SAMPLE_CFG))


if __name__ == "__main__":
    unittest.main()
