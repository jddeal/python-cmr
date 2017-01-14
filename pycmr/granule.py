"""
Module for anything related to Granule searching
"""

from requests import get


class GranuleQuery(object):
    """
    Class for querying CMR for Granules
    """

    base_url = "https://cmr.earthdata.nasa.gov/search/granules.json"
    params = {}
    options = {}

    def __init__(self):
        pass

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

    def temporal(self, date_from, date_to):
        """
        Set the temporal bounds for the query.

        Dates should be provided as ISO 8601 formatted strings.

        :param date_from: earliest date of temporal range
        :param date_to: latest date of temporal range
        :returns: GranueQuery instance
        """

        if not date_from or not date_to:
            return

        self.params["temporal[]"] = "{},{}".format(date_from, date_to)

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
