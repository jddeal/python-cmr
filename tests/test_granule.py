import unittest
import urllib
from pycmr.granule import GranuleQuery

class TestGranuleClass(unittest.TestCase):

    short_name_val = "MOD09GA"
    short_name = "short_name"

    version_val = "006"
    version = "version"

    point_val = "44.6,-63.6"
    point = "point"
    point_space_val = '44.6,                                         -63.6'

    def test_short_name(self):
        query = GranuleQuery()
        query.short_name(self.short_name_val)

        self.assertIn(self.short_name, query.params)
        self.assertEqual(query.params[self.short_name], self.short_name_val)

    def test_version(self):
        query = GranuleQuery()
        query.version(self.version_val)

        self.assertIn(self.version, query.params)
        self.assertEqual(query.params[self.version], self.version_val)

    def test_point(self):
        query = GranuleQuery()
        query.point(self.point_val)

        self.assertIn(self.point, query.params)
        self.assertEqual(urllib.parse.unquote(query.params[self.point]), urllib.parse.unquote(self.point_val))

    def test_point_encoding(self):
        query = GranuleQuery()
        query.point(self.point_val)

        self.assertEqual(query.params[self.point], urllib.parse.quote(self.point_val))

    def test_point_spaces(self):
        query = GranuleQuery()
        query.point(self.point_space_val)

        self.assertEqual(query.params[self.point], urllib.parse.quote(self.point_val))

if __name__ == '__main__':
    unittest()
