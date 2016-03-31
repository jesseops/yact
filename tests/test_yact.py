import os
import unittest
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

    def test_interaction(self):
        config = yact.from_file(self.SAMPLE_CFG)
        self.assertIsInstance(config.sections, list)
        self.assertEqual(config.get('db'), config['db'])
        config.set('ham', {'spam': True})
        config._data['ham']['eggs'] = {'bar': 1}
        config.remove('environment')
        with self.assertRaises(yact.ConfigEditFailed):
            config.environment = 'development'
        with self.assertRaises(KeyError):
            env = config['environment']
        config.set('environment', 'development')
        self.assertEqual(config['environment'], 'development')
        config.save()

    def test_set(self):
        config = yact.from_file(self.SAMPLE_CFG)
        config.set('set', 'go')
        self.assertEqual(config['set'], 'go')
        config.set('this.must.nest', True)
        self.assertEqual(config.get('this.must.nest'), True)


    def test_get(self):
        config = yact.from_file(self.SAMPLE_CFG)
        self.assertEqual(config.get('ham.eggs.bar'), 1)
        self.assertEqual(config['ham']['eggs']['bar'], 1)

    def test_environment(self):
        config = yact.from_file(self.SAMPLE_CFG)


if __name__ == "__main__":
    unittest.main()
