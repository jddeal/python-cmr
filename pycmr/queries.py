"""
Class contains all queries used on CMR
"""

try:
    from urllib.parse import quote
except ImportError:
    from urllib import pathname2url as quote

from datetime import datetime
from requests import get

class Query(object):
    """
    Base class for all queries
    """

    base_url = ""

    def __init__(self, base_url):
        self.params = {}
        self.options = {}
        self.base_url = base_url

    def _urlencodestring(self, value):
        """
        Returns a URL-Encoded version of the given value parameter
        """
        return quote(value)

    def online_only(self, online_only):
        """
        Set the online_only value for the query.

        Must be of type Boolean
        """

        if not isinstance(online_only, bool):
            raise TypeError("Online_only must be of type bool")

        self.params['online_only'] = online_only

        return self

    def temporal(self, date_from, date_to, exclude_boundary=False):
        """
        Add temporal bounds for the query.
        Dates can be provided as a datetime objects or ISO 8601 formatted strings. Multiple
        ranges can be provided by successive calls to this method before calling execute().
        :param date_from: earliest date of temporal range
        :param date_to: latest date of temporal range
        :param exclude_boundary: whether or not to exclude the date_from/to in the matched range
        :returns: GranueQuery instance
        """

        iso_8601 = "%Y-%m-%dT%H:%M:%SZ"

        # process each date into a datetime object
        def convert_to_string(date):
            """
            Returns the argument as an ISO 8601 or empty string.
            """

            if not date:
                return ""

            try:
                # see if it's datetime-like
                return date.strftime(iso_8601)
            except AttributeError:
                try:
                    # maybe it already is an ISO 8601 string
                    datetime.strptime(date, iso_8601)
                    return date
                except TypeError:
                    raise ValueError(
                        "Please provide None, datetime objects, or ISO 8601 formatted strings."
                    )

        date_from = convert_to_string(date_from)
        date_to = convert_to_string(date_to)

        # if we have both dates, make sure from isn't later than to
        if date_from and date_to:
            if date_from > date_to:
                raise ValueError("date_from must be earlier than date_to.")

        # good to go, make sure we have a param list
        if "temporal" not in self.params:
            self.params["temporal"] = []

        self.params["temporal"].append("{},{}".format(date_from, date_to))

        if exclude_boundary:
            self.options["temporal"] = {
                "exclude_boundary": True
            }

        return self

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

        # CMR does not support any spaces in the point parameter
        point = point.replace(' ', '')
        point = self._urlencodestring(point)

        self.params['point'] = point
        return self

    def downloadable(self, downloadable):
        """
        Set the downloadable value for the query.

        Must be of type Boolean
        """
        if not isinstance(downloadable, bool):
            raise TypeError("Downloadable must be of type bool")

        self.params['downloadable'] = downloadable

        return self

    def entry_title(self, entry_title):
        """
        Set the entry_title value for the query
        """

        entry_title = self._urlencodestring(entry_title)

        self.params['entry_title'] = entry_title

        return self

    def query(self):
        """
        Execute the query we have built and return the JSON that we are sent
        """

        # encode params
        formatted_params = []
        for key, val in self.params.items():

            # list params require slightly different formatting
            if isinstance(val, list):
                for list_val in val:
                    formatted_params.append("{}[]={}".format(key, list_val))
            else:
                formatted_params.append("{}={}".format(key, val))

        params_as_string = "&".join(formatted_params)

        # encode options
        formatted_options = []
        for param_key in self.options:
            for option_key, val in self.options[param_key].items():

                # all CMR options must be booleans
                if not isinstance(val, bool):
                    raise ValueError("parameter '{}' with option '{}' must be a boolean".format(
                        param_key,
                        option_key
                    ))

                formatted_options.append("options[{}][{}]={}".format(
                    param_key,
                    option_key,
                    val
                ))

        options_as_string = "&".join(formatted_options)

        url = "{}?{}&{}".format(self.base_url, params_as_string, options_as_string)

        response = get(url)
        return response.json()

class GranuleQuery(Query):
    """
    Class for querying CMR for Granules
    """

    def __init__(self):
        Query.__init__(self, "https://cmr.earthdata.nasa.gov/search/granules.json")

    def orbit_number(self, orbit1, orbit2=None):
        """"
        Set the orbit_number value for the query
        """

        if orbit2:
            self.params['orbit_number'] = self._urlencodestring(
                '{},{}'.format(str(orbit1), str(orbit2))
            )
        else:
            self.params['orbit_number'] = orbit1

        return self

    def day_night_flag(self, day_night_flag):

        """
        Set the day_night_flag value for the query
        """

        if not isinstance(day_night_flag, str):
            raise TypeError("day_night_flag must be of type str.")

        day_night_flag = day_night_flag.lower()

        if day_night_flag not in ['day', 'night', 'unspecified']:
            raise ValueError("day_night_flag must be day, night or unspecified.")

        self.params['day_night_flag'] = day_night_flag
        return self

    def cloud_cover(self, min_cover=0, max_cover=100):
        """
        Set the cloud cover value for the query
        """

        if not min_cover and not max_cover:
            raise ValueError("Please provide atleast min_cover, max_cover or both")

        if min_cover and max_cover:
            try:
                minimum = float(min_cover)
                maxiumum = float(max_cover)

                if minimum > maxiumum:
                    raise ValueError("Please ensure min cloud cover is lower than max cloud cover")
            except ValueError:
                raise ValueError("Please ensure min_cover and max_cover are both floats")

        self.params['cloud_cover'] = "{},{}".format(min_cover, max_cover)
        return self

    def instrument(self, instrument=""):
        """
        Set the instrument value for the query
        """

        if not instrument:
            raise ValueError("Please provide a value for instrument")

        self.params['instrument'] = instrument
        return self

    def platform(self, platform=""):
        """
        Set the platform value for the query
        """

        if not platform:
            raise ValueError("Please provide a value for platform")

        self.params['platform'] = platform
        return self

    def granule_ur(self, granule_ur=""):
        """
        Set the granule_ur value for the query
        """

        if not granule_ur:
            raise ValueError("Please provide a value for platform")

        self.params['granule_ur'] = granule_ur
        return self

class CollectionsQuery(Query):
    """
    Class for quering CMR for collections
    """

    def __init__(self):
        Query.__init__(self, "https://cmr.earthdata.nasa.gov/search/collections.json")

    def first_ten(self):
        """
        Returns the first 10 results from a basic CMR collection search.
        """

        response = get(self.base_url)
        collections = response.json()["feed"]["entry"]

        return collections
