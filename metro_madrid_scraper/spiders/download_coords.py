import os
import urllib3
from bs4 import BeautifulSoup
from metro_madrid_scraper.constants import CoordScraperConst


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_root_path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), ".."), ".."))


def download_coords_files():
    response = _get_response(CoordScraperConst.URL + CoordScraperConst.URN)
    soup = BeautifulSoup(response.data, 'html5lib')
    transport_list = _get_transport_tag_list(soup)
    metro_urn_type_list = _get_metro_urn_type_list(transport_list)
    _start_download(metro_urn_type_list)


def _get_response(uri):
    http = urllib3.PoolManager()
    return http.request('GET', uri, preload_content=False)


def _get_metro_urn_type_list(transport_list):
    return [tuple((tag.select_one('ul').find('a', {'class': 'ico-kml'}, href=True)['href'],
                   tag.select_one('p').text.lower()))
            for tag in transport_list if 'metro' in tag.select_one('p').text.lower()]


def _get_transport_tag_list(soup):
    return [tag for tag in soup.find_all('li', {'class': 'asociada-item'}) if tag.select_one('p')]


def _start_download(urn_type_tuple_list):
    [_download_file(CoordScraperConst.URL + urn, metro_type) for urn, metro_type in urn_type_tuple_list]


def _download_file(file_uri, file_name):
    response = _get_response(file_uri)
    _create_coord_dir()
    file_name = _get_kml_filename(file_name)
    file_path = os.path.join(_root_path, CoordScraperConst.COORD_DIRECTORY, file_name)
    data = response.read()
    with open(file_path, 'wb') as out:
        out.write(data)


def _get_kml_filename(file_name):
    return file_name.replace(' ', '_') + '.kml'


def _create_coord_dir():
    os.makedirs(os.path.join(_root_path, CoordScraperConst.COORD_DIRECTORY), exist_ok=True)
