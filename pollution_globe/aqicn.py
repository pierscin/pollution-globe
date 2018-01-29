import json
import re
from typing import List, Dict, Union, Tuple, Optional

import requests

headers = {'user-agent': 'pollution-globe/0.1'}


class Aqi:
    """Valid aqi measurement.

    Object is by default sortable by aqi value.
    """

    max_value = 999

    def __init__(self, aqi, date_time, name, id, geo):
        self.aqi = min(aqi, Aqi.max_value)  # type: int
        self.date_time = date_time          # type: str

        self.place = {                      # type: Dict[str, Union[int, str]]
            'id': id,
            'name': name,

            'lat': geo[0],
            'lng': geo[1]
        }

    def __eq__(self, other): return self.aqi == other.aqi

    def __lt__(self, other): return self.aqi < other.aqi


class AqiRepository:
    """Provides aqi data directly from aqicn website."""

    @staticmethod
    def get_data() -> Tuple[Aqi, ...]:
        return tuple(Aqi(o['aqi'], o['utime'], o['city'], o['id'], o['geo']) for o in data_from_website())


def get_raw_world_data():
    """Get raw data from aqi website"""
    stations_data_regex = re.compile(r"mapInitWithData\((\[.*?\])\)")
    return re.search(stations_data_regex, requests.get("http://aqicn.org/map/world/", headers=headers).text).group(1)


def data_from_website(adapter=None) -> List[Dict]:
    """Get data from website as a list of mappings without corrupt entries.

    Args:
        adapter: function transforming data from website to desired form. If none, default adapter is used.

    Returns:
        List of mappings without empty entries. Using default data adapter results in mapping appropriate for Aqi
        objects construction. Example:
        [
            {
                'aqi': 999,
                'utime': '2018-01-29 19:00:00',
                'city': 'Jinan',
                'id': 1505,
                'geo': ['36.650997', '117.120497']
            }
        ]

    """

    def default_world_data_adapter(obj: Dict) -> Optional[Dict]:
        to_replace = {'x': 'id',
                      'g': 'geo'}

        standard_item = {}

        for k, v in obj.items():
            if k in to_replace: standard_item[to_replace[k]] = v
            else: standard_item[k] = v

        mandatory_fields = {"aqi", "utime", "geo", "city", "id"}

        if standard_item.keys() != mandatory_fields: return None

        try:
            standard_item['aqi'] = int(standard_item['aqi'])  # pierscin: sometimes aqi has "weird" values

            if standard_item['aqi'] < 0:
                raise ValueError
        except ValueError:
            return None

        for i, g in enumerate(standard_item['geo']):
            try:
                if isinstance(g, str):
                    coord = re.sub(r"\s+", "", g, flags=re.UNICODE)  # pierscin: sometimes whitespaces in the middle
                    float(coord)  # pierscin: only to check if number is valid
                elif isinstance(g, float):
                    coord = str(g)
                else:
                    raise ValueError

                standard_item['geo'][i] = coord
            except ValueError:
                return None

        return standard_item

    objects = json.loads(get_raw_world_data(), object_hook=adapter if adapter else default_world_data_adapter)

    return [o for o in objects if o is not None]
