import os
import unittest
from figgypudding import Pudding, ConfigEditFailed

class test_FiggyPudding(unittest.TestCase):
    SAMPLE_CFG = os.path.join(os.path.curdir, 'sample.conf')

    def test_from_file(self):
        """
        Check instantiation from path, filename
        """
        test_files = ['test.conf', os.path.join(os.path.curdir, 'test.conf')]
        for tf in test_files:
            config = Pudding.from_file(tf, 'tests')
            self.assertIsInstance(config, Pudding)

    def test_interaction(self):
        config = Pudding.from_file(self.SAMPLE_CFG)
        self.assertIsInstance(config.sections, list)
        self.assertEqual(config.get('db'), config['db'])
        config.set('pudding', {'yummy': True})
        config._data['pudding']['foo'] = {'bar': 1}
        config.remove('environment')
        with self.assertRaises(ConfigEditFailed):
            config.environment = 'development'
        with self.assertRaises(KeyError):
            env = config['environment']
        config.set('environment', 'development')
        self.assertEqual(config['environment'], 'development')
        config.save()

    def test_set(self):
        config = Pudding.from_file(self.SAMPLE_CFG)
        config.set('set', 'go')
        self.assertEqual(config['set'], 'go')
        config.set('this.must.nest', True)
        self.assertEqual(config.get('this.must.nest'), True)


    def test_get(self):
        config = Pudding.from_file(self.SAMPLE_CFG)
        self.assertEqual(config.get('pudding.foo.bar'), 1)
        self.assertEqual(config['pudding']['foo']['bar'], 1)


if __name__ == "__main__":
    unittest.main()