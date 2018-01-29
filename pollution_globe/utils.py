from typing import Sequence, List, Union

from pollution_globe.aqicn import Aqi


def pollution_grade(aqi: int) -> int:
    """Translate aqi levels to pollution grade."""
    if         aqi <=  50: return 0
    elif  50 < aqi <= 100: return 1
    elif 100 < aqi <= 150: return 2
    elif 150 < aqi <= 200: return 3
    elif 200 < aqi <= 300: return 4
    else:                  return 5


def normalize_data_for_globe(data: Sequence[Aqi]) -> List[Union[str, float, int]]:
    """Chrome globe expects flat list of data in form: [lat1, lng1, float[0-1], color_id, lat2, lng2, ...]."""
    res = []

    for d in data:
        res.append(d.place['lat'])
        res.append(d.place['lng'])

        res.append(min(d.aqi / Aqi.max_value,  1))
        res.append(pollution_grade(d.aqi))

    return res
