import json
import logging
from urllib.parse import urlencode
import pyproj


class Search:

    def __init__(self, json_string: str):
        parsed_json = json.loads(json_string)
        self.max_rating = parsed_json.get("max_rating")
        self.min_rating = parsed_json.get("min_rating")
        self.max_ascent = parsed_json.get("max_ascent")
        self.min_ascent = parsed_json.get("min_ascent")
        self.max_duration = parsed_json.get("max_duration")
        self.min_duration = parsed_json.get("min_duration")
        self.act = parsed_json.get("act")
        self.geo = parsed_json.get("geo")

    def url(self):
        params = {"bbox": create_bounding_box(self.geo, 10),
                  "act": self.act,
                  "time": "{},{}".format(self.min_duration, self.max_duration),
                  "hdif": "{},{}".format(self.min_ascent, self.max_ascent),
                  global_rating_attribute[self.act]: "{}-,{}+".format(self.min_rating, self.min_rating)}
        return "https://www.camptocamp.org/routes?{}".format(urlencode(params))

def create_bounding_box(gps_coordinates, radius):
    transformer = pyproj.Transformer.from_crs(original_crs, target_crs, always_xy=True)
    center = transformer.transform(gps_coordinates["long"], gps_coordinates["lat"])
    # print(center)
    radius = radius * 1000
    # print(radius)
    return "{},{},{},{}".format(center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)

global_rating_attribute = {
    "skitouring": "lrat",  # F - ED7
    "rock_climbing": "grat",  # F - ED7
    "snow_ice_mixed": "grat",  # F - ED7
    "mountain_climbing": "grat",  # F - ED7
    "ice_climbing": "grat",  # F - ED7
    "hiking": "hrat",  # T1-T5
    "snowshoeing": "wrat",  # W1-W5
    "mountain_biking": "mdbr",  # V1-V6
    "via_ferrata": "krat"  # K1-K6
}

target_crs = pyproj.CRS('EPSG:3857')  # web mercator
original_crs = pyproj.CRS('EPSG:4326')  # WGS84
