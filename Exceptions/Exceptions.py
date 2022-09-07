import json


class MissingArgumentsException(Exception):
    def __init__(self, missing_args):
        super().__init__(missing_args)
        self.missing_args = missing_args

    def __str__(self):
        return f"Missing Required Or Invalid Arguments (lat, lng). Provided: {', '.join(self.missing_args)}"


class NoInterestsForRegionException(Exception):
    def __init__(self, property_region):
        super().__init__(property_region)
        self.property_region = property_region

    def __str__(self):
        return f"No Interests For {self.property_region}."