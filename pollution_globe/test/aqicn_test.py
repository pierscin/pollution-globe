from random import shuffle
from unittest.mock import MagicMock

import pytest

base_data = '{{"aqi":{aqi},"utime":"2018-01-30 23:00:00","city":"Yantai","x":1509,"g":[{lat},"121.447935"]}}'
lat = '"37.463822"'


@pytest.fixture
def aqicn_with_mock_world_data():
    import pollution_globe.aqicn

    pollution_globe.aqicn.get_raw_world_data = MagicMock(name='get_raw_world_data')

    return pollution_globe.aqicn


def test_proper_aqi_representations_in_json(aqicn_with_mock_world_data):
    string_aqi = '"101"'
    int_aqi = '50'

    aqicn_with_mock_world_data.get_raw_world_data.return_value = '['\
                                                                 + base_data.format(aqi=string_aqi, lat=lat) + ',' \
                                                                 + base_data.format(aqi=int_aqi, lat=lat) + ']'

    data = list(aqicn_with_mock_world_data.AqiRepository.get_data())

    assert len(data) == 2

    data.sort()

    assert data[0].aqi == 50
    assert data[1].aqi == 101


def test_invalid_entries_should_be_deleted_from_result(aqicn_with_mock_world_data):
    correct_aqi = '10'

    placeholder_aqi = base_data.format(aqi='"placeholder"', lat=lat)
    invalid_aqi = base_data.format(aqi='"-"', lat=lat)
    invalid_lat = base_data.format(aqi=correct_aqi, lat='"12.xx"')
    no_city = '{"aqi":103,"utime":"2018-01-30 23:00:00","x":1509,"g":["120.2","121.447935"]}'

    correct_entry = base_data.format(aqi=correct_aqi, lat=lat)

    only_one_correct_entry = [placeholder_aqi, invalid_aqi, invalid_lat, no_city, correct_entry]

    shuffle(only_one_correct_entry)

    aqicn_with_mock_world_data.get_raw_world_data.return_value = '[' + ','.join(only_one_correct_entry) + ']'

    data = aqicn_with_mock_world_data.AqiRepository.get_data()

    assert len(data) == 1
    assert data[0].aqi == int(correct_aqi)
