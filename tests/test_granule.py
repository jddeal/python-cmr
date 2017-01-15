import unittest
from pycmr.granule import GranuleQuery

class TestGranuleClass(unittest.TestCase):

    short_name_val = "MOD09GA"
    short_name = "short_name"

    version_val = "006"
    version = "version"

    point_val = "44.6,-63.6"
    point = "point"

    online_only = "online_only"
    downloadable = "downloadable"
    entry_id = "entry_title"
    orbit_number = "orbit_number"
    day_night_flag = "day_night_flag"

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

    def test_online_only_set(self):
        query = GranuleQuery()
        query.online_only(True)

        self.assertIn(self.online_only, query.params)
        self.assertEqual(query.params[self.online_only], True)

    def test_online_only_invalid(self):
        query = GranuleQuery()
        query.online_only("Invalid Type")

        self.assertNotIn(self.online_only, query.params)

    def test_downloadable_set(self):
        query = GranuleQuery()
        query.downloadable(True)

        self.assertIn(self.downloadable, query.params)
        self.assertEqual(query.params[self.downloadable], True)

    def test_downloadable_invalid(self):
        query = GranuleQuery()
        query.downloadable("Invalid Type")

        self.assertNotIn(self.downloadable, query.params)

    def test_entry_title_set(self):
        query = GranuleQuery()
        query.entry_title("DatasetId 5")

        self.assertIn(self.entry_id, query.params)
        self.assertEqual(query.params[self.entry_id], "DatasetId%205")

    def test_orbit_number_set(self):
        query = GranuleQuery()
        query.orbit_number(985)

        self.assertIn(self.orbit_number, query.params)
        self.assertEqual(query.params[self.orbit_number], 985)

    def test_orbit_number_encode(self):
        query = GranuleQuery()
        query.orbit_number("985,986")

        self.assertIn(self.orbit_number, query.params)
        self.assertEqual(query.params[self.orbit_number],"985%2C986")

    def test_day_night_flag_day_set(self):
        query = GranuleQuery()
        query.day_night_flag('day')

        self.assertIn(self.day_night_flag, query.params)
        self.assertEqual(query.params[self.day_night_flag], 'day')

    def test_day_night_flag_night_set(self):
        query = GranuleQuery()
        query.day_night_flag('night')

        self.assertIn(self.day_night_flag, query.params)
        self.assertEqual(query.params[self.day_night_flag], 'night')

    def test_day_night_flag_unspecified_set(self):
        query = GranuleQuery()
        query.day_night_flag('unspecified')

        self.assertIn(self.day_night_flag, query.params)
        self.assertEqual(query.params[self.day_night_flag], 'unspecified')

    def test_day_night_flag_invalid_set(self):
        query = GranuleQuery()
        query.day_night_flag('invaliddaynight')

        self.assertNotIn(self.day_night_flag, query.params)

    def test_day_night_flag_invalid_type_set(self):
        query = GranuleQuery()
        query.day_night_flag(True)

        self.assertNotIn(self.day_night_flag, query.params)

if __name__ == '__main__':
    unittest()
