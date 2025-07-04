from __future__ import annotations

import requests

from mooch.location.exceptions import LocationError


class Location:
    def __init__(self, zip_code: int | None = None) -> None:
        """Initialize a Location instance with the specified zip code.

        Args:
            zip_code (int): The zip code to associate with this location.

        """
        if zip_code is None:
            error_message = "zip_code must be provided to initialize a Location instance."
            raise LocationError(error_message)

        self.zip_code = zip_code
        self.city = None
        self.state = None
        self.state_abbreviation = None
        self.latitude = None
        self.longitude = None
        self._load_from_zip_code()

    def load(self):
        # To be deprecated. Leave this method for backward compatibility until next major release.
        return self

    def _load_from_zip_code(self) -> None:
        """Load and populate the location data (city, state, state abbr., lat, long) from the Zippopotam.us API."""
        url = f"https://api.zippopotam.us/us/{self.zip_code}"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:  # noqa: PLR2004
            message = f"Invalid zip code {self.zip_code}."
            raise LocationError(message)

        data = res.json()
        self.city = data["places"][0]["place name"]
        self.state = data["places"][0]["state"]
        self.state_abbreviation = data["places"][0]["state abbreviation"]
        self.latitude = data["places"][0]["latitude"]
        self.longitude = data["places"][0]["longitude"]
