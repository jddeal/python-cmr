"""
Module for anything related to Granule searching
"""

from datetime import datetime
from requests import get


class GranuleQuery(object):
    """
    Class for querying CMR for Granules
    """

    base_url = "https://cmr.earthdata.nasa.gov/search/granules.json"

    def __init__(self):
        self.params = {}
        self.options = {}

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

        if not date_from or not date_to:
            return

        iso_8601 = "%Y-%m-%dT%H:%M:%SZ"

        # process each date into a datetime object
        def convert_to_datetime(date):
            """
            Returns a datetime object from an unknown date-like object.
            """

            try:
                date.strftime(iso_8601)
            except AttributeError:
                try:
                    # try to interpret it as an ISO 8601 string
                    date = datetime.strptime(date, iso_8601)
                except TypeError:
                    raise ValueError(
                        "Please provide datetime objects or ISO 8601 formatted strings."
                    )

            return date

        date_from = convert_to_datetime(date_from)
        date_to = convert_to_datetime(date_to)

        # can't have the 'from' date be more recent than the 'to' date
        if date_from > date_to:
            raise ValueError("date_from must be earlier than date_to.")

        # good to go
        if "temporal" not in self.params:
            self.params["temporal"] = []

        self.params["temporal"].append(
            "{},{}".format(
                date_from.strftime(iso_8601),
                date_to.strftime(iso_8601)
            )
        )

        if exclude_boundary:
            self.options["temporal"] = {
                "exclude_boundary": True
            }

        return self

    def execute(self):
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
