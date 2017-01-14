import unittest
from datetime import datetime

from pycmr.granule import GranuleQuery

class TestGranuleClass(unittest.TestCase):

    short_name_val = "MOD09GA"
    short_name = "short_name"

    version_val = "006"
    version = "version"

    point_val = "44.6,-63.6"
    point = "point"

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
        self.assertEqual(query.params[self.point], self.point_val)

    def test_temporal(self):
        query = GranuleQuery()

        # invalid string formats
        with self.assertRaises(ValueError):
            query.temporal("2016", "2016-10-20T01:02:03Z")
            query.temporal("2016-10-20T01:02:03Z", "2016")

        # unsupported types
        with self.assertRaises(ValueError):
            query.temporal(1, 2)
            query.temporal(None, None)

        # valid parameters
        query.temporal("2016-10-10T01:02:03Z", "2016-10-12T09:08:07Z")
        self.assertIn("temporal[]", query.params)
        self.assertEqual(query.params["temporal[]"], "2016-10-10T01:02:03Z,2016-10-12T09:08:07Z")

        query.temporal("2016-10-10T01:02:03Z", datetime(2016, 10, 12, 9))
        self.assertIn("temporal[]", query.params)
        self.assertEqual(query.params["temporal[]"], "2016-10-10T01:02:03Z,2016-10-12T09:00:00Z")

        query.temporal(datetime(2016, 10, 12, 10, 55, 7), datetime(2016, 10, 12, 9))
        self.assertIn("temporal[]", query.params)
        self.assertEqual(query.params["temporal[]"], "2016-10-12T10:55:07Z,2016-10-12T09:00:00Z")
