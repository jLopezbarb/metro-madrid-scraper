import multiprocessing
import os
import requests

from bs4 import BeautifulSoup
from metro_madrid_scraper.models import Line,Station
from metro_madrid_scraper.constants import MetroScraperConst


def get_metro_info():
    return _scrap_skeleton(_get_lines, MetroScraperConst.URL)


def _scrap_skeleton(procedure, uri):
    retries = 0
    try:
        response = requests.get(uri, MetroScraperConst.HEADERS)
        if response.status_code == 200:
            return procedure(response)
        else:
            print('Requests status metro_madrid_scraper for {0} was {1}'.format(uri, str(response.status_code)))
    except requests.exceptions.Timeout:
        print('Timeout exception on {0}'.format(uri))
        if retries < 3:
            _scrap_skeleton(procedure, uri)
    except requests.exceptions.TooManyRedirects:
        print('It seems that {0} is not correct'.format(uri))
    except requests.exceptions.RequestException as e:
        print(e)


def _get_lines(response):
    soup = BeautifulSoup(response.content, 'lxml')
    lines_section = soup.find('section', {'id': 'block-metro-network-status-block'})
    lines_tags = lines_section.find_all('a', href=True)
    lines_urls = [tuple((_get_stations, MetroScraperConst.URL + a_tag['href'])) for a_tag in lines_tags]
    with multiprocessing.Pool(os.cpu_count()) as p:
        lines = p.starmap(_scrap_skeleton, lines_urls)
    return lines


def _get_stations(response):
    soup = BeautifulSoup(response.content, 'lxml')
    line_name = soup.find('title').text
    line_name = line_name[:line_name.find('|')].strip()
    stations_div = soup.find('div', {'id': 'line-main'})
    metro_type = _set_metro_type(line_name)
    stations_info = [_get_station_info(station) for station in stations_div.find_all('li')]
    return Line(line_name, metro_type, stations_info)


def _set_metro_type(line_name):
    if line_name.startswith('Línea'):
        metro_type = 'Metro'
    elif line_name.startswith('ML'):
        metro_type = 'Metro Ligero'
    else:
        metro_type = 'Ramal'
    return metro_type


def _get_station_info(station_info_div):
    station_name = station_info_div.select_one('a > p').text
    station_rate_zone = station_info_div.select_one('span.icon-tarifa').text
    if station_rate_zone.strip() == '':
        station_rate_zone = 'Tarifa especial de aeropuerto'
    conections = _get_conections(station_info_div)
    correspondences = _get_correspondences(station_info_div)
    station_services = _get_station_services(station_info_div)
    return Station(station_name, station_rate_zone, station_services, correspondences, conections)


def _get_conections(station_info_div):
    if station_info_div.select_one('div.box__line-conexiones'):
        conection_soup = station_info_div.select_one('div.box__line-conexiones')
        return [_clean_alt_attribute(conection['alt']) for conection in conection_soup.select('img')]
    return []


def _get_correspondences(station_info_div):
    if station_info_div.select_one('div.box__line-correspondencias'):
        correspondence_soup = station_info_div.select_one('div.box__line-correspondencias')
        return[_clean_alt_attribute(conection['alt']) for conection in correspondence_soup.select('img')]
    return []


def _get_station_services(station_info_div):
    if station_info_div.select_one('div.box__info-linea--estaciones'):
        station_services_tags = station_info_div.select_one('div.box__info-linea--estaciones') \
            .find_all('div', {'class': ['text__info-estacion',
                                        'text__info-estacion--tit-icon']})
        return [tag.text.strip() for tag in station_services_tags]
    return []


def _clean_alt_attribute(tag):
    return tag.replace('icono ', '').replace('-', ' ')
