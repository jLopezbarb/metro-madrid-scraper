import io
import multiprocessing
import os
import re
import shutil

import unidecode as unidecode
from bs4 import BeautifulSoup

from metro_madrid_scraper.constants import KmlSwitcher
from metro_madrid_scraper.models import Coord

_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def set_coords(metro_info):
    with multiprocessing.Pool(KmlSwitcher.CPU_CORES) as process:
        metro_info = process.map(_set_coord_to_line, metro_info)
    shutil.rmtree(os.path.abspath(os.path.join(_root_path,'coord_files')), ignore_errors=True)
    return metro_info


def _set_coord_to_line(line_info):
    file_path = _get_kml_file_from_metro_type(line_info.metro_type)
    kml_data = _read_kml(file_path)
    line_number = _get_line_number(line_info.name)
    kml_line_stations = _get_line_stations_kml(kml_data, line_number)
    for station in line_info.stations:
        station_coord = None
        station_name = station.name
        if KmlSwitcher.METRO_NAMES.get(station.name.lower(), None) is not None:
            station_name = KmlSwitcher.METRO_NAMES.get(station.name.lower())
        for kml_station in kml_line_stations:
            kml_station_name = re.sub('avda\.', 'avenida', kml_station[0].lower())
            if _is_same_station(kml_station_name, station_name.lower()):
                lat, long = kml_station[1].strip().split(',')
                station_coord = Coord(lat, long)
        if station_coord is not None:
            station.coord = station_coord
    return line_info


def _get_line_number(line_name):
    if line_name.startswith('Ramal'):
        return 'R'
    else:
        return re.search(r'\d+', line_name).group()


def _kml_to_name_coords(line_placemarks):
    placemark = [tuple((placemark.select_one('name').text, placemark.select_one('coordinates').text))
                 for placemark in line_placemarks]
    return [(re.sub('^\d*\w?', '', name).strip(), (coordinates))
            for name, coordinates in placemark]


def _get_line_stations_kml(kml_data, line_number):
    coord_soup = BeautifulSoup(kml_data, 'lxml')
    placemarks = coord_soup.select('placemark')
    line_placemarks = [placemark for placemark in placemarks
                       if placemark.select_one('name').text.startswith(line_number)]
    kml_to_tuple = _kml_to_name_coords(line_placemarks)
    return kml_to_tuple


def _get_kml_file_from_metro_type(metro_type):
    if metro_type == 'Metro' or metro_type == 'Ramal':
        return os.path.abspath(os.path.join(os.path.join(_root_path, "coord_files"), "metro.kml"))
    else:
        return os.path.abspath(os.path.join(os.path.join(_root_path, "coord_files"), "metro_ligero.kml"))


def _read_kml(file):
    with io.open(file, encoding='latin-1') as f:
        data = f.read()
        f.close()
    return data


def _is_same_station(xml_station, metro_station):
    return unidecode.unidecode(xml_station) == unidecode.unidecode(metro_station)


def _set_correct_station(metro_station):
    if KmlSwitcher.get_new_station_name(metro_station) is not None:
        metro_station = KmlSwitcher.get_new_station_name(metro_station)
    return metro_station
