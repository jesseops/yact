import os
import unittest
from figgypudding import Pudding

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
        config.save()


if __name__ == "__main__":
    unittest.main()
