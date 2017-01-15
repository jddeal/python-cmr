"""
Module for anything related to Granule searching
"""

import urllib
from requests import get


class GranuleQuery(object):
    """
    Class for querying CMR for Granules
    """

    base_url = "https://cmr.earthdata.nasa.gov/search/granules.json"

    def __init__(self):
        self.params = {}

    def short_name(self, short_name=None):
        """
        Set the shortName of the product we are querying
        """

        if not short_name:
            return

        self.params['short_name'] = short_name

        return self

    def version(self, version=None):
        """
        Set the version of the product we are querying
        """

        if not version:
            return

        self.params['version'] = version
        return self

    def point(self, point=None):
        """
        Set the point of the search we are querying
        """

        if not point:
            return

        self.params['point'] = point

        return self

    def downloadable(self, downloadable):
        """
        Set the downloadable value for the query.

        Must be of type Boolean
        """
        if not isinstance(downloadable, bool):
            return

        self.params['downloadable'] = downloadable

    def online_only(self, online_only):
        """
        Set the online_only value for the query.

        Must be of type Boolean
        """

        if not isinstance(online_only, bool):
            return

        self.params['online_only'] = online_only

    def entry_title(self, entry_title):
        """
        Set the entry_title value for the query
        """

        entry_title = urllib.parse.quote(entry_title)

        self.params['entry_title'] = entry_title

    def orbit_number(self, orbit_number):
        """"
        Set the orbit_number value for the query
        """

        if isinstance(orbit_number, int):
            self.params['orbit_number'] = orbit_number
        else:
            orbit_number = urllib.parse.quote(orbit_number)
            self.params['orbit_number'] = orbit_number

    def day_night_flag(self, day_night_flag):
        """
        Set the day_night_flag value for the query
        """

        if not isinstance(day_night_flag, str):
            return

        day_night_flag = day_night_flag.lower()

        if day_night_flag not in ['day', 'night', 'unspecified']:
            return

        self.params['day_night_flag'] = day_night_flag

    def execute(self):
        """
        Execute the query we have built and return the JSON that we are sent
        """

        formatted_params = []
        for key, val in self.params.items():
            formatted_params.append("{}={}".format(key, val))

        params_as_string = "&".join(formatted_params)

        url = "{}?{}".format(self.base_url, params_as_string)

        response = get(url)
        return response.json()
